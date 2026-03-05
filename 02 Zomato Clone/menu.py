from typing import List, Optional
import uuid
from models import Item


class Menu:
    def __init__(self, items: Optional[List[Item]] = None) -> None:
        self.items = items if items is not None else []

    def add_item(self, item: Item) -> None:
        if item in self.items:
            raise ValueError(f"Item {item.name} already exists in menu")
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        if item not in self.items:
            raise ValueError(f"Item {item.name} not found in menu")
        self.items.remove(item)

    def update_item(self, old_item: Item, new_item: Item) -> None:
        try:
            index = self.items.index(old_item)
            self.items[index] = new_item
        except ValueError:
            raise ValueError(f"Item {old_item.name} not found in menu")

    def get_items(self) -> List[Item]:
        return self.items.copy()

    def get_item_by_name(self, name: str) -> Optional[Item]:
        for item in self.items:
            if item.name == name:
                return item
        return None

    def get_item_by_id(self, id: str) -> Optional[Item]:
        for item in self.items:
            if item.id == id:
                return item
        return None


class Restaurant:
    def __init__(self, name: str, menu: Menu, location: "Location", id: str | None = None) -> None:
        if not name:
            raise ValueError("Restaurant name cannot be empty")
        if menu is None:
            raise ValueError("Restaurant must have a menu")
        if location is None:
            raise ValueError("Restaurant must have a location")
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.menu = menu
        self.location = location
        self.is_active = True

    def get_menu(self) -> Menu:
        return self.menu

    def get_location(self) -> "Location":
        return self.location

    def __repr__(self) -> str:
        return f"Restaurant(id={self.id}, name={self.name}, loc={self.location})"
