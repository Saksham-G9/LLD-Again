from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str


class INotification(ABC):
    def __init__(self, data: dict[str, str]):
        self.data = data

    @abstractmethod
    def notify(self, user: User):
        ...


class SMSNotification(INotification):
    def notify(self, user: User):
        print(f"Notification sent {self.data} by SMS to {user.name}")


class GmailNotification(INotification):
    def notify(self, user: User):
        print(f"Notification sent {self.data} by Gmail to {user.name}")


class INotificationDecorator(INotification):
    def __init__(self, notification: INotification, headers: dict[str, str] | None = None):
        # Decorator delegates data to the wrapped notification by default
        super().__init__(notification.data)
        self.notification = notification
        self.headers = headers or {"key": "value"}


class NotificationWithHeaders(INotificationDecorator):
    def set_headers(self, headers: dict[str, str]):
        self.headers = headers

    def notify(self, user: User):
        # Merge headers into the wrapped notification's data then forward
        self.notification.data.update(self.headers)
        self.notification.notify(user)


class NotificationService:
    def __init__(self, user: User) -> None:
        self.notifications = []
        self.user = user

    def add_notification(self, notification):
        self.notifications.append(notification)

    def notify(self):
        for notification in self.notifications:
            notification.notify(self.user)


if __name__ == "__main__":
    user = User(id=1, name="Saksham Gupta", email="saksham.gupta@orange.com")

    notification_service = NotificationService(user=user)

    sms = SMSNotification({"message": "Hi", "content": "Hello There"})
    gmail = GmailNotification({"message": "Hi", "content": "Hello There"})
    gmail_with_headers = NotificationWithHeaders(gmail)

    notification_service.add_notification(sms)
    notification_service.add_notification(gmail_with_headers)

    notification_service.notify()
