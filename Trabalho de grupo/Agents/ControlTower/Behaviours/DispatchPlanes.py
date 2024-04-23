import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio


class DispatchPlanes(OneShotBehaviour):
    async def run(self):
        # Despacha-se primeiro os aviões que estão na fila de descolagem, para que não haja deadlocks nas aterragens em que não tem espaço no hangar, logo não aterrando, e bloquando a descolagem
        # Ao despachar os aviões que estão na fila de descolagem, liberta-se o máximo de espaço possível para conseguir fazer aterrar os aviões em espera de aterrar.
        while True:
            if self.agent.takeoff_queue_empty():
                break
            reserved = self.agent.reserve_runway()
            #* Se não houver maneira de aterrar, não faz sentido continuar, retornando e esperando por uma nova chamada do behaviour
            if not reserved:
                return
            plane_req = self.agent.pop_from_takeoff_queue() 
            if plane_req is None: # Não há aviões para descolar
                self.agent.release_runway() # Liberta a runway para o avião que era suposto descolar, mas já foi despachado
                break
            plane_jid, trip = plane_req
            #* Enviar mensagem de descolagem ao avião
            msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
            await self.send(msg)
            # Não é preciso release_runway pq o avião é que indica quando acaba de descolar e liberta a runway
        while True:
            if self.agent.landing_queue_empty():
                break
            reserved = self.agent.reserve_runway()
            if not reserved:
                return
            plane_jid = self.agent.pop_from_landing_queue()
            if plane_jid is None: # Não há aviões para aterrar
                self.agent.release_runway() # Liberta a runway para o avião que era suposto aterrar, mas já foi despachado
                break
            #* Enviar mensagem de confirmação de aterragem ao avião
            msg = Message(to=plane_jid, metadata={"performative": "confirm"}, body=jsonpickle.encode(None))
            await self.send(msg)
            # Não é preciso release_runway pq o avião é que indica quando acaba de aterrar e liberta a runway
