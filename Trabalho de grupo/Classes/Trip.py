import random
import sys
import Utils.GeoDistance as geo

class Trip:
    cur_id = 1
    def __init__(self, origin, destination, type_flight = "normal"):
        # self.c_id = random.randint(0, 10000)
        self.c_id = Trip.cur_id
        Trip.cur_id += 1
        self.origin = origin # String
        self.destination = destination # String
        try:
            self.distance = geo.calculate_distance(origin, destination)
        except:
            print(f"!!!Error calculating distance between {origin} and {destination}. USING STANDARD!!1")
            self.distance = 500
        self.type_flight = type_flight
    
    def get_origin(self) -> str:
        return self.origin
    
    def get_destination(self) -> str:
        return self.destination

    def get_locations(self) -> tuple:
        return self.origin, self.destination
    
    def get_id(self) -> int:
        return self.c_id
    
    def get_distance(self) -> float:
        return self.distance
    
    def get_type_flight(self) -> str:
        return self.type_flight

    @staticmethod    
    def generate_random_trip(locations):
        origin = random.choice(locations)
        destination = random.choice(locations)
        while destination == origin:
            destination = random.choice(locations)
        return Trip(origin, destination)


    def __str__(self):
        string = f"'{self.c_id}'-({self.origin} -> {self.destination})"
        if self.type_flight != "normal":
            string += "*" # Asterisco indica que a viagem é de balanceamento de carga dos hangares
        return string
    
    def __repr__(self) -> str:
        string = f"'{self.c_id}'-({self.origin} -> {self.destination})"
        if self.type_flight != "normal":
            string += "*" # Asterisco indica que a viagem é de balanceamento de carga dos hangares
        return string

if __name__ == "__main__":
    trip = Trip("Lisboa", "Porto")
    print(trip)
    print(f"Distance: {trip.get_distance()} km")  # Output: Distance: 313.0 km