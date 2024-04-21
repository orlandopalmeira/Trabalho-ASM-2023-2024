import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        
        # Mensagem vinda do hangar que contém o avião e a trip #> Use case 1: passo 3
        if msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "hangar": 
            # Interpretação da mensagem
            msg_body = jsonpickle.decode(msg.body)
            plane_jid = msg_body['plane_jid']
            trip = msg_body['trip']
            print(f"{self.agent.name}: Received takeoff request from {cfg.get_jid_name(msg.sender)} for {cfg.get_jid_name(plane_jid)} {trip}")

            # Lógica de descolagem
            await self.order_plane_to_takeoff(plane_jid, trip)

        # Confirmação da descolagem #> Use case 1: passo 5
        elif msg.metadata["performative"] == "confirm" and cfg.identify(msg.sender) == "plane":
            # Interpretação da mensagem
            plane_jid = jsonpickle.decode(msg.body)
            self.agent.release_runway()
            print(f"Plane took-off {cfg.get_jid_name(msg.sender)} ({trip})")

    async def order_plane_to_takeoff(self, plane_jid, trip):
        reserved = self.agent.reserve_runway() #> Use case 1: passo 4
        while not reserved:
            print(f"{self.agent.name}: {plane_jid} for trip {trip} is waiting for a runway to be available.")
            await asyncio.sleep(3)
            reserved = self.agent.reserve_runway()
        msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
        await self.send(msg) #> Use case 1: passo 4



    # without constant checking of the runway availability #! WIP
    async def order_plane_to_takeoff_v2(self, plane_jid, trip):
        reserved = self.agent.reserve_runway() #> Use case 1: passo 4
        while not reserved:
            print(f"{self.agent.name}: {plane_jid} for trip {trip} is waiting for a runway to be available.")
            await asyncio.sleep(5)
            reserved = self.agent.reserve_runway()
        msg = Message(to=plane_jid, body=jsonpickle.encode(trip), metadata={"performative": "inform"})
        await self.send(msg) #> Use case 1: passo 4