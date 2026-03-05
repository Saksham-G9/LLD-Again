import math


class Location:
    def __init__(self, latitude: float, longitude: float) -> None:
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other: "Location") -> float:
        earth_radius_km = 6371
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(other.latitude)
        delta_lat = math.radians(other.latitude - self.latitude)
        delta_lon = math.radians(other.longitude - self.longitude)
        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        return earth_radius_km * c

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Location):
            return False
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __hash__(self) -> int:
        return hash((self.latitude, self.longitude))

    def __repr__(self) -> str:
        return f"Location({self.latitude}, {self.longitude})"
