from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle, sys
sys.path.append("./")
from Classes.Trip import Trip
from Config import Config as cfg

class ReceiveFlightsBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()
        if not msg:
            print("No message received")
            return
        trip = jsonpickle.decode(msg.body)
        print(f"{self.agent.location} received flight: {trip}")


