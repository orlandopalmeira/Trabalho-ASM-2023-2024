import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio


class DispatchPlanes(OneShotBehaviour):
    atom_lock = asyncio.Lock()

    async def run(self):
        # Despacha-se primeiro os aviões que estão na fila de descolagem, para que não haja deadlocks nas aterragens em que não tem espaço no hangar, logo não aterrando, e bloquando a descolagem.
        # Ao despachar os aviões que estão na fila de descolagem, liberta-se o máximo de espaço possível para conseguir fazer aterrar os aviões em espera de aterrar.
        await DispatchPlanes.atom_lock.acquire()
        try:
            while True:
                if self.agent.takeoff_queue_empty():
                    break
                reserved = self.agent.reserve_runway_for_takeoff() #! TEM DE SER UM RESERVERUNWAY DIFERENTE
                #* Se não houver maneira de aterrar, não faz sentido continuar, retornando e esperando por uma nova chamada do behaviour
                if not reserved:
                    return
                self.agent.increase_hangar_availability() # O avião que vai descolar vai libertar um lugar no hangar
                plane_req = self.agent.pop_from_takeoff_queue()
                plane_jid, trip = plane_req
                #* Enviar mensagem de descolagem ao avião
                msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
                await self.send(msg)
                # Não é preciso release_runway pq o avião é que indica quando acaba de descolar e liberta a runway
            while True:
                if self.agent.landing_queue_empty():
                    break
                reserved = self.agent.reserve_runway_for_landing()
                if not reserved:
                    return
                self.agent.decrease_hangar_availability() # O avião que vai aterrar vai ocupar um lugar no hangar
                plane_jid = self.agent.pop_from_landing_queue()
                #* Enviar mensagem de confirmação de aterragem ao avião
                msg = Message(to=plane_jid, metadata={"performative": "confirm"}, body=jsonpickle.encode(None))
                await self.send(msg)
                # Não é preciso release_runway pq o avião é que indica quando é que liberta a runway ao acabar de aterrar
        finally:
            DispatchPlanes.atom_lock.release()

#* TRATADO
#? Tecnicamente pode haver uma incongruência se houver dois aviões para aterrar e houver runways disponiveis para ambos, mas apenas um hangar disponivel, é possivel que duas threads verifiquem na reserve_runway que é possivel aterrarem ambos, no entanto não haver espaço.
# A solução passaria por ter um lock na função reserve_runway, mais concretamente um lock a englobar a verificação da possibilidade de reserva e a alteração no valor da hangar_availability. Isto irá fazer com que a reserve_runway tenha de passar a receber algum argumento que indique se deva aumentar ou reduzir a hangar_availability
#* (Adotada) Outra solução mais fácil, seria meter um lock como variavel de classe da DispatchPlanes, fazendo com que cada vez que o run era chamado, era garantido que apenas uma thread correria. Isto simplificaria a estrutura do código da DispatchPlanes também.