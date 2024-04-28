from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Config import Config as cfg
from Utils.Prints import *
import asyncio
import jsonpickle
import requests


class SendMeteo(PeriodicBehaviour):

    async def run(self):
        self.print("Sending meteo...")
        for city in self.agent.cities:
            pass