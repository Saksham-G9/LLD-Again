from dataclasses import dataclass, field
from enum import Enum
from typing import List
import uuid


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Item:
    name: str
    image_path: str
    price: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.name:
            raise ValueError("Item name cannot be empty")


@dataclass(frozen=True)
class OrderItem:
    name: str
    price_at_order: int
    quantity: int


class Order:
    _order_counter = 0

    def __init__(self, items: List[OrderItem], restaurant: "Restaurant") -> None:
        if not items:
            raise ValueError("Order must contain at least one item")
        Order._order_counter += 1
        self.order_id = Order._order_counter
        self.items = items
        self.restaurant = restaurant
        self.status = OrderStatus.PENDING
        self.total_price = sum(i.price_at_order * i.quantity for i in items)

    def get_items(self) -> List[OrderItem]:
        return self.items.copy()

    def get_status(self) -> OrderStatus:
        return self.status

    def update_status(self, new_status: OrderStatus) -> None:
        if not isinstance(new_status, OrderStatus):
            raise ValueError("Status must be an OrderStatus value")
        self.status = new_status

    def get_total_price(self) -> int:
        return self.total_price

    def __repr__(self) -> str:
        return f"Order(ID={self.order_id}, Status={self.status.value}, Total={self.total_price})"
