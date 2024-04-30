from spade.behaviour import CyclicBehaviour
from spade.message import Message

import jsonpickle
import asyncio

from Classes.Trip import Trip
from Config import Config as cfg

from Agents.Plane.Behaviors.ExecuteFlight import ExecuteFlight


class RecvRequests(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # self.agent.print(f"No message received", "yellow")
            return
        msg_body = jsonpickle.decode(msg.body)
        
        # 1.4. A **CT** envia mensagem para descolar ao **Plane**. (performative: *inform*, body: *Trip*)
        if msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "ct": 
            trip = msg_body
            self.agent.set_trip(trip)
            self.agent.add_behaviour(ExecuteFlight())

        # 2.2. A **CT** verifica se as condições permitem aterrar, e envia mensagem de confirmação ao **Plane**. (performative: *confirm*, body: *None*)
        elif msg.metadata["performative"] == "confirm" and cfg.identify(msg.sender) == "ct":
            LANDING_TIME = self.agent.LANDING_TIME
            await asyncio.sleep(LANDING_TIME)
            destination = self.agent.trip.get_destination()
            self.agent.print(f"Finished landing at {destination}")
            self.agent.set_landed()
            self.agent.set_trip(None)

            # 3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)
            hangar_destin = cfg.get_hangar_jid(destination)
            ct_destin = cfg.get_ct_jid(destination)
            plane_jid = str(self.agent.jid)
            msg = Message(to=ct_destin, metadata={"performative": "inform"}, body=jsonpickle.encode(self.agent.jid))
            await self.send(msg)
            msg = Message(to=hangar_destin, metadata={"performative": "inform"}, body=jsonpickle.encode(self.agent.jid))
            await self.send(msg)
            

