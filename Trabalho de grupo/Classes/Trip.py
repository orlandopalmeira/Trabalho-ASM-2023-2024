import random
import sys, os
import time
import json
import Utils.GeoAPI as geo
from Config import Config as cfg

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

        #* Objeto com timestamps relativas ao voo para posterior processamento
        self.flight_stats = {
            "init": time.time(),
            "takeoff": None,
            "destination_arrival": None,
            "landed": None, 
        }
    
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
    
    def get_flight_stats(self) -> dict:
        return self.flight_stats
    
    def ts_takeoff(self):
        self.flight_stats["takeoff"] = time.time()

    def ts_destination_arrival(self):
        self.flight_stats["destination_arrival"] = time.time()

    def ts_landing(self):
        self.flight_stats["landed"] = time.time()

    def generate_report(self):
        # file_name = f"resources/flights.json"
        file_name = cfg.stats_file_name()

        stats = dict()

        # Calculate time spent waiting for takeoff, flying and landing
        stats["id"] = self.c_id
        stats["flight"] = f"{self.origin} -> {self.destination}"
        stats["waiting_takeoff"] = round(self.flight_stats["takeoff"] - self.flight_stats["init"], 2)
        # stats["flying"] = round(self.flight_stats["destination_arrival"] - self.flight_stats["takeoff"], 2)
        stats["waiting_landing"] = round(self.flight_stats["landed"] - self.flight_stats["destination_arrival"], 2)

        # Treat timestamps to dates
        # for key in self.flight_stats:
        #     if self.flight_stats[key] is not None:
        #         self.flight_stats[key] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.flight_stats[key]))


        # Check if file is empty
        if not os.path.exists(file_name):
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump([], f)

        # Load file
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(file_name, 'w', encoding='utf-8') as f:
            data.append(stats)
            json.dump(data, f, indent=4, ensure_ascii=False)

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