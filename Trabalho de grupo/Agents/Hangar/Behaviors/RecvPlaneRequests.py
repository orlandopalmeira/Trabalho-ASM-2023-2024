from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
# from Config import Config as cfg

class RecvPlaneRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        
        msg_body = jsonpickle.decode(msg.body)
        if msg.metadata["performative"] == "request" and msg_body['type'] == 'plane_request': #> Recebeu um pedido de avião
            print(f"Received plane request from {msg.sender}")
            await self.send_plane(str(msg.sender))
    
    async def send_plane(self, sender):
        if self.agent.planes:
            plane = self.agent.planes.pop(0)
            msg_body = {
                'type': 'plane_from_hangar',
                'plane': plane
            }

            msg = Message(to=sender, body=jsonpickle.encode(msg_body), metadata={"performative": "accept"})
            await self.send(msg)
            print(f"Sent plane {plane} to {sender}")
        else:
            msg_body = {
                'type': 'plane_from_hangar'
            }
            msg = Message(to=sender, body=jsonpickle.encode(msg_body), metadata={"performative": "refuse"})
            await self.send(msg)

