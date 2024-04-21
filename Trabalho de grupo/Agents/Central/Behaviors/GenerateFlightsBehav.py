from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg

class GenerateFlightsBehav(PeriodicBehaviour):
    async def run(self):
        trips = []
        for _ in range(self.agent.num_of_flights_per_interval):
            trip = Trip.generate_random_trip(self.agent.airport_locations)
            trips.append(trip)

        # Pretty Printing das viagens geradas
        print()
        for trip in trips:
            print("CENTRAL: Flight generated", trip)
        print()
        ###
        
        for trip in trips:
            airport_name = cfg.get_airport_jid(trip.get_origin())
            msg = Message(to=airport_name, metadata={'performative':'request'}, body=jsonpickle.encode(trip))
            await self.send(msg) #> Use case 1: passo 1
