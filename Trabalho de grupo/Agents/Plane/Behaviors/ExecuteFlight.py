from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

# from Agents.Plane.Behaviors.PlaneRequest import PlaneRequest

class ExecuteFlight(OneShotBehaviour):

    async def run(self):
        #> Descolagem do avião
        TEMPO_DE_DESCOLAGEM = self.agent.TAKEOFF_TIME
        await asyncio.sleep(TEMPO_DE_DESCOLAGEM)
        # Mensagem de confirmação de descolagem
        destin = cfg.get_ct_jid(self.agent.get_location())
        msg = Message(to=destin, body=jsonpickle.encode("avião"), metadata={"performative": "confirm"})
        await self.send(msg)
        self.agent.set_flying()

        #> Voo do avião
        # Simulação de demora de tempo
        distance = self.agent.get_trip().get_distance()
        tempo = self.agent.CONVERSION_KM_TO_SECS * distance
        tempo = round(tempo, 2)
        self.agent.print(f"Starting flight to {self.agent.trip.get_destination()} ({distance} km) (time: {tempo}s)")
        await asyncio.sleep(tempo)


        #> Aterragem do avião
        destination = self.agent.get_trip().get_destination()
        ct_jid = cfg.get_ct_jid(destination)
        
        # Pedido de aterragem à CT destino
        msg = Message(to=ct_jid, 
                      metadata={"performative": "request"},
                      body=jsonpickle.encode(str(self.agent.jid)))
        await self.send(msg)



