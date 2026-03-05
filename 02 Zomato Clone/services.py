from typing import Optional, List
from models import OrderItem, Order


class PaymentService:
    def process_payment(self, user_id: str, amount: int) -> bool:
        raise NotImplementedError()


class NotificationService:
    def send_notification(self, user_id: str, message: str) -> None:
        raise NotImplementedError()


class DefaultPaymentService(PaymentService):
    def process_payment(self, user_id: str, amount: int) -> bool:
        if amount <= 0:
            return False
        print(f"Processing payment of {amount} for user {user_id}")
        return True


class DefaultNotificationService(NotificationService):
    def send_notification(self, user_id: str, message: str) -> None:
        print(f"Notification for user {user_id}: {message}")


class OrderService:
    def __init__(self, payment_service: Optional[PaymentService] = None, notification_service: Optional[NotificationService] = None) -> None:
        self.payment_service = payment_service or DefaultPaymentService()
        self.notification_service = notification_service or DefaultNotificationService()

    def place_order(self, user: "User", restaurant: "Restaurant") -> Optional[Order]:
        if user.cart.is_empty():
            print("Cart is empty. Cannot place order.")
            return None
        if user.cart.restaurant is None or user.cart.restaurant.id != restaurant.id:
            raise ValueError("Cart restaurant does not match the restaurant for this order")
        total_price = user.cart.get_total_price()
        if not self.payment_service.process_payment(str(user.user_id), total_price):
            print("Payment failed. Please try again.")
            return None
        snapshot_items: List[OrderItem] = [OrderItem(i.name, i.price, qty) for i, qty in user.cart.get_items()]
        order = Order(snapshot_items, restaurant)
        user.orders.append(order)
        user.cart.clear()
        self.notification_service.send_notification(str(user.user_id), f"Your order #{order.order_id} has been placed at {restaurant.name}! Total: {order.get_total_price()}")
        return order
