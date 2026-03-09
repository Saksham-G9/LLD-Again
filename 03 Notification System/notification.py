from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, is_dataclass
import logging
from typing import TypeVar, Generic, Any

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str


# Channel-specific typed data structures
@dataclass(frozen=True)
class SMSData:
    phone: str
    message: str
    content: str


@dataclass(frozen=True)
class EmailData:
    to_email: str
    subject: str
    message: str
    content: str


@dataclass(frozen=True)
class PopUpData:
    title: str
    message: str
    content: str


DataT = TypeVar("DataT")


class INotification(Generic[DataT], ABC):
    def __init__(self, data: DataT):
        # data is typed per-channel (dataclass or mapping)
        self.data: DataT = data

    @abstractmethod
    def notify(self, user: User): ...


class SMSNotification(INotification[SMSData]):
    def notify(self, user: User) -> None:
        print(f"Notification sent {self.data} by SMS to {user.name}")


class GmailNotification(INotification[EmailData]):
    def notify(self, user: User) -> None:
        print(f"Notification sent {self.data} by Gmail to {user.name}")


# New notification channel: PopUpNotification
class PopUpNotification(INotification[PopUpData]):
    def notify(self, user: User) -> None:
        print(f"Notification sent {self.data} by PopUp to {user.name}")


class INotificationDecorator(INotification[DataT], Generic[DataT]):
    def __init__(
        self, notification: INotification[DataT], headers: dict[str, str] | None = None
    ):
        # Decorator delegates data to the wrapped notification by default
        super().__init__(notification.data)
        self.notification: INotification[DataT] = notification
        self.headers = headers or {"key": "value"}


class NotificationWithHeaders(INotificationDecorator):
    def set_headers(self, headers: dict[str, str]):
        self.headers = headers

    def notify(self, user: User):
        # Merge headers into a copy of the wrapped notification's data then forward
        original = self.notification.data
        try:
            if is_dataclass(original):
                merged = {**asdict(original), **self.headers}
            elif isinstance(original, dict):
                merged = {**original, **self.headers}
            else:
                # fallback: try to use object's __dict__
                merged = {**vars(original), **self.headers}

            # Temporarily set merged data, call notify, then restore original to avoid side-effects
            self.notification.data = merged  # type: ignore[assignment]
            self.notification.notify(user)
        finally:
            self.notification.data = original


class IPersistence:
    def persist(self, notification: INotification): ...


class LogsStorage(IPersistence):
    def persist(self, notification: INotification[Any]):
        payload = notification.data
        if is_dataclass(payload):
            payload = asdict(payload)
        logging.info(
            f"Notification saved in logs channel={notification.__class__.__name__} data={payload}"
        )


class NotificationService:
    def __init__(self, user: User, persistence: IPersistence) -> None:
        self.notifications = []
        self.user = user
        self.persistence = persistence

    def add_notification(self, notification):
        self.notifications.append(notification)

    def notify(self):
        for notification in self.notifications:
            notification.notify(self.user)
            self.persistence.persist(notification)


if __name__ == "__main__":
    user = User(id=1, name="Saksham Gupta", email="saksham.gupta@orange.com")
    persistence = LogsStorage()

    notification_service = NotificationService(user=user, persistence=persistence)

    sms = SMSNotification(
        SMSData(phone="+1234567890", message="Hi", content="Hello There")
    )
    gmail = GmailNotification(
        EmailData(
            to_email=user.email,
            subject="Greetings",
            message="Hi",
            content="Hello There",
        )
    )
    gmail_with_headers = NotificationWithHeaders(gmail)

    popup = PopUpNotification(
        PopUpData(title="Welcome", message="Hi", content="Hello There")
    )

    notification_service.add_notification(sms)
    notification_service.add_notification(gmail_with_headers)
    notification_service.add_notification(popup)

    notification_service.notify()
