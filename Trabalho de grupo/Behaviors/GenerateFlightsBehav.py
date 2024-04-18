# Basic template for a behaviour file

from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour, Behaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Utils.TripGenerator import generate_random_trip

class GenerateFlightsBehav(PeriodicBehaviour):
    async def run(self):
        print(f'Central: Generating flights')
        for i in range(self.agent.num_of_flights_per_interval):
            trip = generate_random_trip(self.agent.airport_locations)
            print(f'Agent {self.agent.jid}: Sending trip: {trip}')
            await self.send(Message(to=str(self.agent.central_jid), metadata={'performative':'request'}, body=jsonpickle.encode(trip)))
