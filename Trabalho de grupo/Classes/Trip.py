import random
import sys
# sys.path.append("./")
import Utils.GeoDistance as geo

class Trip:
    def __init__(self, origin, destination):
        self.c_id = random.randint(0, 10000)
        self.origin = origin
        self.destination = destination
    
    def get_origin(self) -> str:
        return self.origin
    
    def get_destination(self) -> str:
        return self.destination

    def get_locations(self) -> tuple:
        return self.origin, self.destination
    
    def get_id(self) -> int:
        return self.c_id
    
    def get_distance(self) -> float:
        return geo.calculate_distance(self.origin, self.destination)

    @staticmethod    
    def generate_random_trip(locations):
        origin = random.choice(locations)
        destination = random.choice(locations)
        while destination == origin:
            destination = random.choice(locations)
        # return (origin, destination)
        return Trip(origin, destination)


    def __str__(self):
        # return f"({self.c_id}) {self.origin} -> {self.destination}"
        return f"{self.origin} -> {self.destination}"

if __name__ == "__main__":
    trip = Trip("Lisboa", "Porto")
    print(trip)
    print(f"Distance: {trip.get_distance()} km")  # Output: Distance: 313.0 km