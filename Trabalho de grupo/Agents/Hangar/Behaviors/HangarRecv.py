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
            # print("No message received")
            return

        # 1.2. O **aeroporto** envia um pedido de avião ao **hangar**. (performative: *request*, body: *Trip*)
        if msg.metadata["performative"] == "request" and cfg.identify(msg.sender) == "airport":
            trip = jsonpickle.decode(msg.body)
            print(f"{self.agent.name}: Received plane request from {cfg.get_jid_name(msg.sender)} for {trip}")
            plane = await self.get_plane()
            ct_jid = cfg.get_ct_jid(self.agent.location)
            plane_and_trip = {
                'plane_jid': plane, 
                'trip': trip
            }
            msg = Message(to=ct_jid, body=jsonpickle.encode(plane_and_trip), metadata={"performative": "inform"})
            await self.send(msg)

        # 3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            print(f"{self.agent.name}: {cfg.get_jid_name(plane_jid)} estationated.")
            self.agent.add_plane(plane_jid)


    async def get_plane(self): #! Isto talvez fosse melhor se um periodic behaviour
        INTERVAL = 5
        plane = self.agent.pop_plane()
        while plane is None:
            #! Talvez aqui seja o lugar para enviar uma mensagem à central a indicar falta de aviões
            print(f"{self.agent.name} has no planes available. Retrying in {INTERVAL} seconds...")
            await asyncio.sleep(INTERVAL)
            plane = self.agent.pop_plane()
        return plane

