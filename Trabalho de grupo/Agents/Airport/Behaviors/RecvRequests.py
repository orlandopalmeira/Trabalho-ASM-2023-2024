from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        msg_body = jsonpickle.decode(msg.body)
        # print(f"{self.agent.location} received flight: {msg_body}")
        if msg.metadata["performative"] == "request":
            print(f"{self.agent.location} received request: {msg.body}")
        elif msg.metadata["performative"] == "inform":
            print(f"{self.agent.location} received inform: {msg.body}")
        else:
            print(f"{self.agent.location} received message: {msg.body}")
        


