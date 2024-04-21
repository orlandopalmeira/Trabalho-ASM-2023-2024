from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import time

class RecvRequests(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # print("No message received")
            return
        msg_body = jsonpickle.decode(msg.body)
        
        # Aterragem de avião
        if msg.metadata["performative"] == "inform":
            print(f"{self.agent.name}: {cfg.get_jid_name(msg.sender)} landed")
            #! Meter avião no hangar
        # Recebeu um pedido de flight da central #> (Use case 1: passo 1)
        elif msg.metadata["performative"] == "request": 
            trip = msg_body
            print(f"{self.agent.name}: Received flight {trip}")
            self.agent.push_flight(trip)
            #! Não usei o behav PlaneRequest porque não lhe podemos dar argumentos, temos de ver melhor como fazer isto
            hangar_name = cfg.get_hangar_jid(self.agent.location)
            msg = Message(to=hangar_name, body=jsonpickle.encode(trip), metadata={"performative": "request"})
            await self.send(msg) #> Use case 1: passo 2

        #* Versão antiga com dicts
        # Recebeu uma resposta (do hangar) ao pedido de avião feito ao hangar
        # elif msg_body['type'] == 'plane_from_hangar' and msg.metadata["performative"] == "accept":
        #     plane_jid = msg_body['plane']

        #     print(f"{self.agent.name} received {cfg.get_jid_name(plane_jid)} from {msg.sender.localpart}")
        #     trip = self.agent.pop_flight()
        #     # print(f"{plane_jid} starting flight: {trip}")
        #     msg = Message(to=plane_jid, body=jsonpickle.encode(trip), metadata={"performative": "request"})
        #     await self.send(msg)

        # # Recebeu um flight gerado da central
        # elif msg_body['type'] == 'generate_flight' and msg.metadata['performative'] == 'request': 
        #     trip = msg_body['trip']
        #     print(f"{self.agent.name} received flight: {trip}")
        #     self.agent.push_flight(trip)
        #     self.agent.add_behaviour(PlaneRequest()) # Pede um avião ao hangar
            
        else:
            print(f"{self.agent.name}: WARNING received message: {msg.body}!")
        


