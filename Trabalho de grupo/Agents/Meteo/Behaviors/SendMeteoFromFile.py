from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Config import Config as cfg
from Utils.Prints import *
from Agents.Meteo.Meteo import *
from Classes.Weather import Weather


import asyncio
import jsonpickle
import requests
import json


class SendMeteoFromFile(PeriodicBehaviour):

    async def run(self):
        self.agent.print("Sending meteo...")
        meteo_file_name = cfg.meteo_file_name()
        with open(meteo_file_name, 'r') as meteo_file:
            meteo_obj = json.load(meteo_file)

        for city in meteo_obj:
            weather = meteo_obj[city]
            # self.agent.print(f"Sending '{weather}' weather to {city} from file")
            # weather_obj = Weather(weather)
            msg = Message(to=cfg.get_ct_jid(city), body=jsonpickle.encode(weather), metadata={"performative": "inform"})
            await self.send(msg)
