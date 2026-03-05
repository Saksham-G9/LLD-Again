from location import Location
from models import Item
from menu import Menu, Restaurant
from restaurant_manager import RestaurantManager
from user import User


def main() -> None:
    bangalore = Location(12.9716, 77.5946)

    margherita = Item("Margherita", "margherita.jpg", 200)
    garlic_bread = Item("Garlic Bread", "garlic_bread.jpg", 100)
    cheeseburger = Item("Cheeseburger", "cheeseburger.jpg", 150)

    pizza_place = Restaurant("Pizza Place", Menu([margherita, garlic_bread]), Location(12.9716, 77.5946))
    burger_joint = Restaurant("Burger Joint", Menu([cheeseburger]), Location(12.9820, 77.6060))

    rm = RestaurantManager()
    rm.add_restaurant(pizza_place)
    rm.add_restaurant(burger_joint)

    user = User("Alice", bangalore)
    nearby = rm.get_nearby_restaurants(user.location, radius=10)
    print("Nearby Restaurants:")
    for r in nearby:
        print(f" - {r.name}")

    user.add_to_cart(margherita, pizza_place, quantity=2)
    user.add_to_cart(garlic_bread, pizza_place, quantity=1)
    order = user.place_order(pizza_place)
    if order:
        print(order)


if __name__ == "__main__":
    main()
