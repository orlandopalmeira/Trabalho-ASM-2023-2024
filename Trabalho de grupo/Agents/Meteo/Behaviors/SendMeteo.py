from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Config import Config as cfg
from Utils.Prints import *
from Agents.Meteo.MeteoAPI import *
from Classes.Weather import Weather

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
                self.agent.print(f"Sending '{weather}' weather to {city} from {dt}", "dark blue")
                # idx = self.agent.cur_count % len(self.agent.cities[city])
            else:
                weather = get_current_weather(city)
                self.agent.print(f"Sending '{weather}' weather to {city} from current weather", "dark blue")

            weather_obj = Weather(weather)
            msg = Message(to=cfg.get_ct_jid(city), body=jsonpickle.encode(weather_obj), metadata={"performative": "inform"})
            await self.send(msg)

        if self.agent.get_mode() == self.agent.MODE_PAST: # To advance to next time, for next weather in PAST MODE
            # self.agent.cur_timestamp += 3600
            self.agent.next_datetime() # Avança 1 hora
