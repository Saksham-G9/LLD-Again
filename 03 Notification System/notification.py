from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, is_dataclass
import logging
from typing import TypeVar, Generic, Any, Dict, List, Optional

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


class NotificationWithHeaders(INotificationDecorator[DataT], Generic[DataT]):
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


class IPersistence(ABC):
    @abstractmethod
    def persist(self, notification: INotification[Any]) -> None: ...


class LogsStorage(IPersistence):
    def persist(self, notification: INotification[Any]):
        payload = notification.data
        if is_dataclass(payload):
            payload = asdict(payload)
        logging.info(
            f"Notification saved in logs channel={notification.__class__.__name__} data={payload}"
        )


class InMemoryStorage(IPersistence):
    """Simple in-memory persistence for testing / interview demos."""

    def __init__(self) -> None:
        self.saved: List[Dict[str, Any]] = []

    def persist(self, notification: INotification[Any]) -> None:
        payload = notification.data
        if is_dataclass(payload):
            payload = asdict(payload)
        entry: Dict[str, Any] = {
            "channel": notification.__class__.__name__,
            "data": payload,
        }
        self.saved.append(entry)
        logging.info(f"Notification saved in memory {entry}")


@dataclass
class RetryPolicy:
    retries: int = 0
    backoff_seconds: float = 0.0


class NotificationService:
    def __init__(
        self,
        user: User,
        persistence: IPersistence,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self.notifications = []
        self.user = user
        self.persistence = persistence
        self.retry_policy = retry_policy or RetryPolicy()

    def add_notification(self, notification: INotification[Any]) -> None:
        self.notifications.append(notification)

    def notify(self) -> None:
        for notification in self.notifications:  # type: INotification[Any]
            attempt = 0
            while True:
                try:
                    notification.notify(self.user)
                    self.persistence.persist(notification)
                    break
                except Exception as exc:
                    attempt += 1
                    logging.exception(
                        f"Notification failed for {notification.__class__.__name__} attempt={attempt}"
                    )
                    if attempt > self.retry_policy.retries:
                        logging.error(
                            f"Dropping notification after {attempt} attempts: {notification}"
                        )
                        break
                    if self.retry_policy.backoff_seconds:
                        import time

                        time.sleep(self.retry_policy.backoff_seconds)


if __name__ == "__main__":
    user = User(id=1, name="Saksham Gupta", email="saksham.gupta@orange.com")
    # use InMemoryStorage for demo / interview testing
    persistence = InMemoryStorage()
    # simple retry policy: 1 retry with small backoff
    retry_policy = RetryPolicy(retries=1, backoff_seconds=0.1)

    notification_service = NotificationService(
        user=user, persistence=persistence, retry_policy=retry_policy
    )

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

    # show in-memory storage contents for verification
    print("Persisted entries:", persistence.saved)
