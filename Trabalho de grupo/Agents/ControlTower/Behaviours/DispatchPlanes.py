import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio


class DispatchPlanes(OneShotBehaviour): #! WIP
    async def run(self): #! Needs testing
        while True:
            reserved = self.agent.reserve_runway()
            # Se não houver maneira de aterrar, não faz sentido continuar, retornando e esperando por uma nova chamada do behaviour
            if not reserved: 
                return 
            plane_req = self.agent.pop_from_takeoff_queue()
            if plane_req is None: # Não há aviões para descolar
                break
            plane_jid, trip = plane_req
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)
            # Não é preciso release_runway pq o avião é que faz o release
        while True:
            reserved = self.agent.reserve_runway()
            if not reserved:
                return
            plane_req = self.agent.pop_from_landing_queue()
            if plane_req is None: # Não há aviões para aterrar
                break
            plane_jid, trip = plane_req
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)
