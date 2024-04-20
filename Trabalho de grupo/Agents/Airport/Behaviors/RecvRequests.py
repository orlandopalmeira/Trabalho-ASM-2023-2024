from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import time

from Agents.Airport.Behaviors.PlaneRequest import PlaneRequest

class RecvRequests(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        msg_body = jsonpickle.decode(msg.body)
        
        if msg_body['type'] == 'plane_from_hangar': # Recebeu uma resposta (do hangar) ao pedido de avião feito ao hangar
            plane_jid = msg_body['plane']
            if msg.metadata["performative"] == "accept":
                print(f"{self.agent.name} received {cfg.get_jid_name(plane_jid)} from {msg.sender}")
            else:
                print("Mensagem desconhecida RECVEQUESTS!")

        elif msg_body['type'] == 'generate_flight' and msg.metadata['performative'] == 'request': # Recebeu um voo gerado da central
            trip = msg_body['trip']
            print(f"{self.agent.name} received flight: {trip}")
            self.agent.add_behaviour(PlaneRequest()) # Pede um avião ao hangar
            
        else:
            print(f"{self.agent.name} received message: {msg.body}")
        


