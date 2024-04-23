import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio

# from Agents.ControlTower.Behaviours.DispatchPlanes import DispatchPlanes

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # print("No message received")
            return
        
        # 1.3. O **hangar** envia o jid do avião selecionado à **CT**. (performative: *inform*, body: *{plane_jid: String, trip: Trip}*)
        if msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "hangar":
            msg_body = jsonpickle.decode(msg.body)
            plane_jid = msg_body['plane_jid']
            trip = msg_body['trip']
            print(f"{self.agent.name}: Received takeoff request from {cfg.get_jid_name(msg.sender)} for {cfg.get_jid_name(plane_jid)} {trip}")

            # await self.order_plane_to_takeoff_old(plane_jid, trip)
            self.agent.add_to_takeoff_queue(plane_jid, trip) # Adicionar à fila de descolagens (este método irá dar trigger ao behavior DispatchPlanes)

        # 1.5. O **Plane** envia mensagem de confirmação de descolagem à **CT**. (performative: *confirm*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "confirm" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            self.agent.release_runway()
            print(f"{self.agent.name}: Plane took-off {cfg.get_jid_name(msg.sender)}")
        
        # 2.1. O **Plane** envia mensagem de pedido de aterragem à **CT**. (performative: *request*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "request" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            print(f"{self.agent.name}: Received landing request from {cfg.get_jid_name(msg.sender)}")
            self.agent.add_to_landing_queue(plane_jid) # Adicionar à fila de aterragens (este método irá dar trigger ao behavior DispatchPlanes)

        # 2.3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)
        elif msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "plane":
            plane_jid = jsonpickle.decode(msg.body)
            print(f"{self.agent.name}: Plane landed {cfg.get_jid_name(msg.sender)}")
            self.agent.release_runway()

        else:
            print(f"{self.agent.name}: WARNING - Received unknown message from {cfg.get_jid_name(msg.sender)}")


    # OLD VERSION: with constant checking of the runway availability
    # async def order_plane_to_takeoff_old(self, plane_jid, trip):
    #     reserved = self.agent.reserve_runway() 
    #     while not reserved:
    #         print(f"{self.agent.name}: {plane_jid} for trip {trip} is waiting for a runway to be available.")
    #         await asyncio.sleep(3)
    #         reserved = self.agent.reserve_runway()
    #     msg = Message(to=plane_jid, metadata={"performative": "inform"}, body=jsonpickle.encode(trip))
    #     await self.send(msg)


