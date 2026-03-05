from typing import List
from models import Item, Order
from cart import Cart
from services import DefaultPaymentService, DefaultNotificationService, OrderService


class User:
    _user_counter = 0

    def __init__(self, name: str, location: "Location", payment_service=None, notification_service=None) -> None:
        if not name:
            raise ValueError("User name cannot be empty")
        User._user_counter += 1
        self.user_id = User._user_counter
        self.name = name
        self.location = location
        self.cart = Cart()
        self.orders: List[Order] = []
        self.payment_service = payment_service or DefaultPaymentService()
        self.notification_service = notification_service or DefaultNotificationService()

    def add_to_cart(self, item: Item, restaurant: "Restaurant", quantity: int = 1) -> None:
        self.cart.add_item(item, restaurant, quantity)

    def remove_from_cart(self, item: Item) -> None:
        self.cart.remove_item(item)

    def get_cart_total(self) -> int:
        return self.cart.get_total_price()

    def place_order(self, restaurant: "Restaurant") -> Order | None:
        service = OrderService(self.payment_service, self.notification_service)
        return service.place_order(self, restaurant)

    def get_orders(self) -> List[Order]:
        return self.orders.copy()

    def __repr__(self) -> str:
        return f"User(ID={self.user_id}, Name={self.name}, Orders={len(self.orders)})"
