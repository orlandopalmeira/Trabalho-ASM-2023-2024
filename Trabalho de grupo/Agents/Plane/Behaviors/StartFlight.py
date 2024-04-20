from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

# from Agents.Plane.Behaviors.PlaneRequest import PlaneRequest

class StartFlight(OneShotBehaviour):

    async def run(self):
        self.agent.set_flying()
        distance = self.agent.get_trip().get_distance()
        tempo = self.agent.CONVERSION_KM_TO_SECS * distance
        print(f"{self.agent.name} starting flight to {self.agent.trip.get_destination()} ({distance} km) (time: {tempo}s)")
        
        # Simulação de demora de tempo
        await asyncio.sleep(tempo)

        destination = self.agent.get_trip().get_destination()
        destination_jid = cfg.get_airport_jid(destination)
        
        # Mensagem de aviso de chegada ao aeroporto destino
        msg = Message(body=None, 
                      to=destination_jid, 
                      metadata={"performative": "inform"})
        await self.send(msg)



