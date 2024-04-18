from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour, Behaviour
from spade.message import Message
import jsonpickle, sys
sys.path.append("./")
from Classes.Trip import Trip
from Config import Config as cfg

class GenerateFlightsBehav(PeriodicBehaviour):
    async def run(self):
        print(f'Central: Generating flights')
        for _ in range(self.agent.num_of_flights_per_interval):
            trip = Trip.generate_random_trip(self.agent.airport_locations)
            print("Flight generated: ", trip)
            airport_name = cfg.get_airport_jid(trip.get_origin())
            msg = Message(to=airport_name, metadata={'performative':'request'}, body=jsonpickle.encode(trip))
            await self.send(msg)
