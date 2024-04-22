import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio


class DispatchPlanes(OneShotBehaviour):
    async def run(self):
        while True:
            # if self.agent.takeoff_queue_empty():
            #     break
            plane_req = self.agent.pop_from_takeoff_queue() #! Solução do prob de baixo, talvez passe por meter locks dentro desta função e reservar automaticamente a runway dentro desse mesmo lock
            if plane_req is None: # Não há aviões para descolar
                break
            #! Tecnicamente pode existir ocasiao entre estas duas funcoes em que dou pop da queue e depois a runway fica indisponivel, descartando o plane_req
            reserved = self.agent.reserve_runway()
            # Se não houver maneira de aterrar, não faz sentido continuar, retornando e esperando por uma nova chamada do behaviour
            if not reserved: 
                return 
            plane_jid, trip = plane_req
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)
            # Não é preciso release_runway pq o avião é que faz o release
        while True:
            plane_req = self.agent.pop_from_landing_queue()
            if plane_req is None: # Não há aviões para aterrar
                break
            #! Tecnicamente pode existir ocasiao entre estas duas funcoes em que dou pop da queue e depois a runway fica indisponivel, descartando o plane_req
            reserved = self.agent.reserve_runway()
            if not reserved:
                return
            plane_jid, trip = plane_req
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)
