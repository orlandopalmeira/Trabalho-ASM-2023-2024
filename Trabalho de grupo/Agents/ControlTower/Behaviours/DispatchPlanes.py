import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio


class DispatchPlanes(OneShotBehaviour): #! WIP
    async def run(self): #! Needs testing
        for plane_jid, trip in self.agent.queue_takeoffs:
            reserved = self.agent.reserve_runway()
            if not reserved: return False
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)
        for plane_jid, trip in self.agent.queue_takeoffs:
            if not reserved: return False
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)