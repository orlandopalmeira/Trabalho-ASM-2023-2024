import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        
        if msg.metadata["performative"] == "inform": #> Use case 1: passo 3
            msg_body = jsonpickle.decode(msg.body)
            plane_jid = msg_body['plane_jid']
            trip = msg_body['trip']
            print(f"Received takeoff request from hangar {msg.sender} for {plane_jid} ({trip})")
            msg = Message(to=plane_jid, body=jsonpickle.encode(trip), metadata={"performative": "inform"}) 
            await self.send(msg) #> Use case 1: passo 4