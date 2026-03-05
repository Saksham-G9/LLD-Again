from typing import List, Optional
from menu import Restaurant
from location import Location


class RestaurantManager:
    PROXIMITY_RADIUS_KM = 5.0

    def __init__(self) -> None:
        self.restaurants: dict[str, Restaurant] = {}

    def add_restaurant(self, restaurant: Restaurant) -> None:
        if not restaurant:
            raise ValueError("Restaurant cannot be None")
        if restaurant.id in self.restaurants:
            raise ValueError(f"Restaurant {restaurant.id} already exists")
        self.restaurants[restaurant.id] = restaurant

    def remove_restaurant(self, id: str) -> None:
        if id not in self.restaurants:
            raise ValueError(f"Restaurant {id} not found")
        del self.restaurants[id]

    def get_restaurants(self) -> List[Restaurant]:
        return list(self.restaurants.values())

    def get_restaurant(self, id: str) -> Optional[Restaurant]:
        return self.restaurants.get(id)

    def get_nearby_restaurants(self, location: Location, radius: float | None = None) -> List[Restaurant]:
        if radius is None:
            radius = self.PROXIMITY_RADIUS_KM
        if radius <= 0:
            raise ValueError("Radius must be positive")
        nearby = []
        for restaurant in self.restaurants.values():
            if restaurant.is_active:
                distance = restaurant.get_location().distance_to(location)
                if distance <= radius:
                    nearby.append((restaurant, distance))
        nearby.sort(key=lambda x: x[1])
        return [r for r, _ in nearby]
