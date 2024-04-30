from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Config import Config as cfg
from Utils.Prints import *
from Agents.Meteo.Meteo import *

import asyncio
import jsonpickle
import requests


class SendMeteo(PeriodicBehaviour):

    async def run(self):
        # self.agent.print("Sending meteo...")
        for city in self.agent.cities:
            weather = None
            if self.is_past_weather_config():
                idx = self.cur_count
                weather_info = self.agent.cities[city][idx]
                weather = weatherinfo_to_weather(weather_info)
                dt = weather_datetime(weather_info)
                self.agent.print(f"Sending '{weather}' weather to {city} from {dt}")
                idx = self.cur_count % len(self.agent.cities[city])
            else:
                weather = self.get_current_weather(city)
                self.agent.print(f"Sending '{weather}' weather to {city} from current weather")

            msg = Message(to=cfg.get_ct_jid(city), body=jsonpickle.encode(weather), metadata={"performative": "inform"})
            await self.send(msg)
