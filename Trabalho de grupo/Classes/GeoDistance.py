from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class GeoDistance:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="city_distance_calculator")

    def get_coordinates(self, city_name):
        location = self.geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Coordinates for {city_name} not found.")
            return None

    def calculate_distance(self, city1, city2):
        """Retorna a distância entre duas cidades em quilômetros. Caso haja um erro com o nome das cidades, retorna None."""
        coords1 = self.get_coordinates(city1)
        coords2 = self.get_coordinates(city2)

        if coords1 and coords2:
            distance = geodesic(coords1, coords2).kilometers
            distance = round(distance, 2)
        else:
            print(f"ERROR:({city1}-{city2}) Cannot calculate distance due to missing coordinates from one city.")
            distance = None
        return distance


if __name__ == "__main__":
    gd = GeoDistance()
    city1 = "Cabeceiras de Basto"
    city2 = "Nova Zelândia"
    distance = gd.calculate_distance(city1, city2)
    print(f"The distance between {city1} and {city2} is approximately {distance} kilometers.")
