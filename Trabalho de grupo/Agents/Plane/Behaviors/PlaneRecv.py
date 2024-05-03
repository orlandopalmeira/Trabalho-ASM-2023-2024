from spade.behaviour import CyclicBehaviour
from spade.message import Message

import jsonpickle
import asyncio

from Config import Config as cfg
from Classes.Trip import Trip
from Classes.Weather import Weather

from Agents.Plane.Behaviors.ExecuteFlight import ExecuteFlight


class RecvRequests(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # self.agent.print(f"No message received", "red")
            return
        msg_body = jsonpickle.decode(msg.body)
        
        # 1.4. A **CT** envia mensagem para descolar ao **Plane**. (performative: *inform*, body: *{trip: Trip, weather: Weather}*)
        if msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "ct": 
            # msg_body: {"trip": Trip, "weather": Weather}
            trip = msg_body.get("trip")
            weather = msg_body.get("weather")
            weather_str = weather.get_weather()
            self.agent.set_trip(trip)
            self.agent.set_weather_factor_in_takeoff(weather_str)
            self.agent.print(f"Takeoff will take {self.agent.takeoff_time}s, because {weather_str}.", "green")
            self.agent.add_behaviour(ExecuteFlight())

        # 2.2. A **CT** verifica se as condições permitem aterrar, e envia mensagem ao **Plane**. (performative: *confirm*, body: *Weather*)
        elif msg.metadata["performative"] == "confirm" and cfg.identify(msg.sender) == "ct":
            # msg_body: Weather
            weather_str = msg_body.get_weather()
            self.agent.set_weather_factor_in_landing(weather_str)
            self.agent.print(f"Landing will take {self.agent.takeoff_time}s, because {weather_str}.", "green")
            await asyncio.sleep(self.agent.landing_time)
            destination = self.agent.trip.get_destination()
            self.agent.print(f"Finished landing at {destination}", "green")
            self.agent.set_landed()
            self.agent.set_trip(None)

            # 3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)
            hangar_destin = cfg.get_hangar_jid(destination)
            ct_destin = cfg.get_ct_jid(destination)
            plane_jid = str(self.agent.jid)
            msg = Message(to=ct_destin, metadata={"performative": "inform"}, body=jsonpickle.encode(self.agent.jid))
            await self.send(msg)
            msg = Message(to=hangar_destin, metadata={"performative": "inform"}, body=jsonpickle.encode(self.agent.jid))
            await self.send(msg)
            

