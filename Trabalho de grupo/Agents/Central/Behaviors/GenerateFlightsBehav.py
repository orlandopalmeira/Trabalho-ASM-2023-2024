from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg

class GenerateFlightsBehav(PeriodicBehaviour):
    async def run(self):
        # print(f'Central: Generating flights')
        for _ in range(self.agent.num_of_flights_per_interval):
            trip = Trip.generate_random_trip(self.agent.airport_locations)
            print("Flight generated:", trip)
            airport_name = cfg.get_airport_jid(trip.get_origin())
            msg_body = {
                'type': 'generate_flight',
                'trip': trip
            }
            msg = Message(to=airport_name, metadata={'performative':'request'}, body=jsonpickle.encode(msg_body))
            await self.send(msg)
