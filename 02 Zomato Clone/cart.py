from typing import List, Tuple, Optional
from models import Item


class Cart:
    def __init__(self) -> None:
        self.items: dict[Item, int] = {}
        self.restaurant: Optional["Restaurant"] = None

    def add_item(self, item: Item, restaurant: "Restaurant", quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if item is None:
            raise ValueError("Item cannot be None")
        if self.restaurant is None:
            self.restaurant = restaurant
        elif self.restaurant.id != restaurant.id:
            raise ValueError("Cart can only contain items from one restaurant. Clear the cart to switch restaurants.")
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item: Item) -> None:
        if item not in self.items:
            raise ValueError("Item not found in cart")
        del self.items[item]
        if not self.items:
            self.restaurant = None

    def update_quantity(self, item: Item, quantity: int) -> None:
        if quantity <= 0:
            self.remove_item(item)
        elif item in self.items:
            self.items[item] = quantity
        else:
            raise ValueError("Item not found in cart")

    def get_items(self) -> List[Tuple[Item, int]]:
        return list(self.items.items())

    def get_item_count(self) -> int:
        return sum(self.items.values())

    def get_total_price(self) -> int:
        return sum(quantity * item.price for item, quantity in self.items.items())

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def clear(self) -> None:
        self.items.clear()
        self.restaurant = None

    def __repr__(self) -> str:
        return f"Cart({self.get_item_count()} items, Total: {self.get_total_price()})"
