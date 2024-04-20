from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import time

from Agents.Plane.Behaviors.StartFlight import StartFlight

class RecvRequests(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print(f"{self.agent.name}: No message received")
            return
        msg_body = jsonpickle.decode(msg.body)
        
        if msg.metadata["performative"] == "request": # Pedidos do aeroporto para começar uma viagem
            trip = msg_body
            print(f"\n{self.agent.name} starting flight: {trip}\n")
            self.agent.set_trip(trip)
            self.agent.add_behaviour(StartFlight())
