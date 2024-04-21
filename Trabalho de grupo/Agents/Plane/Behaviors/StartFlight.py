from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

# from Agents.Plane.Behaviors.PlaneRequest import PlaneRequest

class StartFlight(OneShotBehaviour):

    async def run(self):
        #> Descolagem do avião
        TEMPO_DE_DESCOLAGEM = 1
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
        print(f"{self.agent.name}: Starting flight to {self.agent.trip.get_destination()} ({distance} km) (time: {tempo}s)")
        await asyncio.sleep(tempo)


        #> Aterragem do avião
        destination = self.agent.get_trip().get_destination()
        destination_jid = cfg.get_airport_jid(destination)
        
        # Mensagem de aviso de chegada ao aeroporto destino
        msg = Message(body=jsonpickle.encode(None), 
                      to=destination_jid, 
                      metadata={"performative": "inform"})
        await self.send(msg)



