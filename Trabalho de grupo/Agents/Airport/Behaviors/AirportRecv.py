from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle

from Classes.Trip import Trip
from Config import Config as cfg
from Utils.Prints import print_c

class RecvRequests(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # print("No message received")
            return
        msg_body = jsonpickle.decode(msg.body)
        
        # Recebeu um pedido de flight da central #> (Use case 1: passo 1)
        if msg.metadata["performative"] == "request": 
            trip = msg_body
            self.agent.print(f"Received flight {trip}")
            hangar_name = cfg.get_hangar_jid(self.agent.location)
            msg = Message(to=hangar_name, body=jsonpickle.encode(trip), metadata={"performative": "request"})
            await self.send(msg) #> Use case 1: passo 2

        else:
            self.agent.print(f"WARNING received unknown message from {msg.sender}!", "red")
        


