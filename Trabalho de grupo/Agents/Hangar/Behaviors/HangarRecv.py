from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

class RecvPlaneRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return

        # Pedido de avião vindo do aeroporto para enviar um avião à control Tower #> Use case 1: passo 2
        if msg.metadata["performative"] == "request":
            trip = jsonpickle.decode(msg.body)
            print(f"Received plane request from {cfg.get_jid_name(msg.sender)} for {trip}")
            plane = await self.get_plane()
            ct_jid = cfg.get_control_tower_jid(self.agent.location)
            plane_and_trip = {
                'plane_jid': plane, 
                'trip': trip
            }
            msg = Message(to=ct_jid, body=jsonpickle.encode(plane_and_trip), metadata={"performative": "inform"}) #> Use case 1: passo 3
            await self.send(msg)


    async def get_plane(self):
        plane = self.agent.pop_plane()
        while plane is None:
            #! Talvez aqui seja o lugar para enviar uma mensagem à central a indicar falta de aviões
            print(f"{self.agent.name} has no planes available. Retrying in 10 seconds...")
            await asyncio.sleep(10)
            plane = self.agent.pop_plane()
        return plane

