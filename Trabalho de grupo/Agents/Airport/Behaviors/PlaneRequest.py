from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
import time

class PlaneRequest(OneShotBehaviour):

    async def run(self):
        hangar_name = cfg.get_hangar_jid(self.agent.location)
        msg_body = {
            'type': 'plane_request'
        }
        msg = Message(to=hangar_name, body=jsonpickle.encode(msg_body), metadata={"performative": "request"})
        # body = RequestPlane(self_id, x_pos, y_pos, x_dest, y_dest) #> Não sei se é necessaria uma classe para isto. Ou sequer um body
        # msg.body = jsonpickle.encode(body)

        await self.send(msg)
            


        #> Parte que será passada para o behaviour de receção de mensagens
        # TIMEOUT = 10
        # msg = await self.receive(timeout=TIMEOUT)
        # if not msg:
        #     print(f"!!!ERROR: Airport {self.agent.name} did not get response from hangar {hangar_name}.!!!")
        #     return
        
        # if msg.metadata["performative"] == "refuse":
        #     print(f"!!!ERROR: Hangar {hangar_name} refused plane request from airport {self.agent.name}.!!!")
        # elif msg.metadata["performative"] == "agree":
        #     print(f"Hangar {hangar_name} agreed to send plane to airport {self.agent.name}.")

