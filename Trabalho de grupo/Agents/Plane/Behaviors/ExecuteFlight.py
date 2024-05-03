from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

class ExecuteFlight(OneShotBehaviour):

    async def run(self):
        #> Descolagem do avião
        await asyncio.sleep(self.agent.takeoff_time)
        # Mensagem de confirmação de descolagem
        destin = cfg.get_ct_jid(self.agent.get_location())
        msg = Message(to=destin, body=jsonpickle.encode(str(self.agent.name)), metadata={"performative": "confirm"})
        await self.send(msg)
        self.agent.set_flying()

        #> Voo do avião
        # Simulação de demora de tempo
        distance = self.agent.get_trip().get_distance()
        tempo = self.agent.CONVERSION_KM_TO_SECS * distance
        tempo = round(tempo, 2)
        self.agent.print(f"Starting flight '{self.agent.get_trip().get_id()}' to {self.agent.get_trip().get_destination()} ({distance} km) (time: {tempo}s)", "green")
        await asyncio.sleep(tempo)


        #> Aterragem do avião
        destination = self.agent.get_trip().get_destination()
        ct_jid = cfg.get_ct_jid(destination)
        
        # Pedido de aterragem à CT destino
        self.agent.set_waiting_landing_perm()
        msg = Message(to=ct_jid, 
                      metadata={"performative": "request"},
                      body=jsonpickle.encode(str(self.agent.jid)))
        await self.send(msg)



