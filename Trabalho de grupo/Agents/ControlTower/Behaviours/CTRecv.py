import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Config import Config as cfg

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        
        # Mensagem vinda do hangar que contém o avião e a trip
        if msg.metadata["performative"] == "inform": #> Use case 1: passo 3
            # Interpretação da mensagem
            msg_body = jsonpickle.decode(msg.body)
            plane_jid = msg_body['plane_jid']
            trip = msg_body['trip']
            print(f"Received takeoff request from hangar {cfg.get_jid_name(msg.sender)} for {cfg.get_jid_name(plane_jid)} ({trip})")

            # Lógica de descolagem
            self.agent.reserve_runway() #> Use case 1: passo 4
            msg = Message(to=plane_jid, body=jsonpickle.encode(trip), metadata={"performative": "inform"}) 
            await self.send(msg) #> Use case 1: passo 4