from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg

class PlaneRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            print("No message received")
            return
        trip = jsonpickle.decode(msg.body)

        async def run(self):
            hangar_name = cfg.get_hangar_jid(self.location)
            msg = Message(to=hangar_name, body="Plane request", metadata={"performative": "request"})
            # body = RequestPlane(self_id, x_pos, y_pos, x_dest, y_dest) #> Não sei se é necessaria uma classe para isto. Ou sequer um body
            # msg.body = jsonpickle.encode(body)

            await self.send(msg)
            print(f"Airport {self.agent.name} requested a plane to hangar {hangar_name}.")
            
            TIMEOUT = 10
            msg = await self.receive(timeout=TIMEOUT)
            if not msg:
                print(f"!!!ERROR: Airport {self.agent.name} did not get response from hangar {hangar_name}.!!!")
                return
            
            if msg.metadata["performative"] == "refuse":
                print(f"!!!ERROR: Hangar {hangar_name} refused plane request from airport {self.agent.name}.!!!")
            elif msg.metadata["performative"] == "agree":
                print(f"Hangar {hangar_name} agreed to send plane to airport {self.agent.name}.")

