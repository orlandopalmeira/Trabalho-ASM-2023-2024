import random
import sys
sys.path.append("./")
import Utils.GeoDistance as geo

class Trip:
    def __init__(self, origin, destination):
        self.c_id = random.randint(0, 10000)
        self.origin = origin
        self.destination = destination
    
    def get_origin(self):
        return self.origin
    
    def get_destination(self):
        return self.destination

    def get_locations(self):
        return self.origin, self.destination
    
    def get_id(self):
        return self.c_id
    
    def distance(self):
        return geo.calculate_distance(self.origin, self.destination)
    
    def __str__(self):
        return f"Trip {self.c_id}: {self.origin} -> {self.destination}"

if __name__ == "__main__":
    trip = Trip("Lisboa", "Porto")
    print(trip)
    print(f"Distance: {trip.distance()} km")  # Output: Distance: 313.0 km