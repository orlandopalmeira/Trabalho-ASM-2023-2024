from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Config import Config as cfg
from Utils.Prints import *
from Agents.Meteo.MeteoAPI import *

import asyncio
import jsonpickle
import requests


class SendMeteo(PeriodicBehaviour):

    async def run(self):
        for city in self.agent.cities:
            weather = None
            if self.agent.get_mode() == self.agent.MODE_PAST:
                # weather_info = self.agent.cities[city][idx]
                weather_info = get_exact_past_weather(city, self.agent.cur_datetime)
                weather = weatherinfo_to_weather(weather_info)
                dt = weather_datetime(weather_info)
                self.agent.print(f"Sending '{weather}' weather to {city} from {dt}", "green")
                # idx = self.agent.cur_count % len(self.agent.cities[city])
            else:
                weather = self.agent.get_current_weather(city)
                self.agent.print(f"Sending '{weather}' weather to {city} from current weather", "green")

            msg = Message(to=cfg.get_ct_jid(city), body=jsonpickle.encode(weather), metadata={"performative": "inform"})
            await self.send(msg)

        if self.agent.get_mode() == self.agent.MODE_PAST: # To advance to next time, for next weather in PAST MODE
            # self.agent.cur_timestamp += 3600
            self.agent.next_datetime() # Avança 1 hora
