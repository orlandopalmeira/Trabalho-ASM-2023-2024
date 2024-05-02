from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

from Agents.Hangar.Behaviors.DispatchFlightReqs import DispatchFlightReqs

class RecvPlaneRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # print("No message received")
            return

        # 1.2. O **aeroporto** envia um pedido de avião ao **hangar**. (performative: *request*, body: *Trip*)
        if msg.metadata["performative"] == "request" and cfg.identify(msg.sender) == "airport":
            trip = jsonpickle.decode(msg.body)
            self.agent.print(f"Received plane request for flight {trip}")
            self.agent.add_waiting_request(trip)
            
        # 3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            self.agent.print(f"{cfg.get_jid_name(plane_jid)} estationated.")
            self.agent.add_plane(plane_jid)


