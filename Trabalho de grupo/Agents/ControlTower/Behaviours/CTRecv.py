import jsonpickle
import asyncio
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Config import Config as cfg

from Classes.Weather import Weather

# from Agents.ControlTower.Behaviours.DispatchPlanes import DispatchPlanes

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # self.agent.print("No message received")
            return
        
        # 1.3. O **hangar** envia o jid do avião selecionado à **CT**. (performative: *inform*, body: *{plane_jid: String, trip: Trip}*)
        if msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "hangar":
            msg_body = jsonpickle.decode(msg.body)
            plane_jid = msg_body['plane_jid']
            trip = msg_body['trip']
            self.agent.print(f"Received takeoff request for {cfg.get_jid_name(plane_jid)} and flight {trip}")

            # await self.order_plane_to_takeoff_old(plane_jid, trip)
            self.agent.add_to_takeoff_queue(plane_jid, trip) # Adicionar à fila de descolagens (este método irá dar trigger ao behavior DispatchPlanes)

        # 1.5. O **Plane** envia mensagem de confirmação de descolagem à **CT**. (performative: *confirm*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "confirm" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            self.agent.release_runway()
            self.agent.print(f"{cfg.get_jid_name(msg.sender)} took-off")
        
        # 2.1. O **Plane** envia mensagem de pedido de aterragem à **CT**. (performative: *request*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "request" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            self.agent.print(f"Received landing request from {cfg.get_jid_name(msg.sender)}")
            self.agent.add_to_landing_queue(plane_jid) # Adicionar à fila de aterragens (este método irá dar trigger ao behavior DispatchPlanes)

        # 2.3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            # self.agent.print(f"{cfg.get_jid_name(msg.sender)} landed.")
            self.agent.release_runway()

        elif msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "meteo":
            weather_obj = jsonpickle.decode(msg.body)
            weather = weather_obj.get_weather()
            self.agent.set_weather(weather)
            # self.agent.print(f"Received weather update from {cfg.get_jid_name(msg.sender)}")

        else:
            self.agent.print(f"WARNING - Received unknown message from {cfg.get_jid_name(msg.sender)}", "red")


    # OLD VERSION: with constant checking of the runway availability
    # async def order_plane_to_takeoff_old(self, plane_jid, trip):
    #     reserved = self.agent.reserve_runway() 
    #     while not reserved:
    #         print(f"{self.agent.name}: {plane_jid} for trip {trip} is waiting for a runway to be available.")
    #         await asyncio.sleep(3)
    #         reserved = self.agent.reserve_runway()
    #     msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
    #     await self.send(msg)

