from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import asyncio

class RecvPlaneRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        
        msg_body = jsonpickle.decode(msg.body)
        if msg.metadata["performative"] == "request" and msg_body['type'] == 'plane_request': #> Recebeu um pedido de avião
            print(f"Received plane request from {msg.sender.localpart}")
            await self.send_plane(str(msg.sender))
    
    async def send_plane(self, sender):
        plane = self.agent.pop_plane()
        while plane is None:
            #! Talvez enviar um pedido de aviões à central
            #! Talvez inves deste sleep, esperar por uma mensagem de chegada de avião e quando essa mensagem chegar, enviar o avião. Do género, ter uma queue de flights no aeroporto e quando chegar um avião, associar esse avião a um flight. E para que o hangar saiba se o seu airport tem alguem à espera pode ter uma variável com o número de pedidos de aviões que recebeu e não respondeu.
            print(f"{self.agent.name} has no planes available. Retrying in 10 seconds...")
            await asyncio.sleep(10)
            plane = self.agent.pop_plane()

        msg_body = {
            'type': 'plane_from_hangar',
            'plane': plane
        }

        msg = Message(to=sender, body=jsonpickle.encode(msg_body), metadata={"performative": "accept"})
        await self.send(msg)
        print(f"Sent {cfg.get_jid_name(plane)} to {cfg.get_jid_name(sender)}")
