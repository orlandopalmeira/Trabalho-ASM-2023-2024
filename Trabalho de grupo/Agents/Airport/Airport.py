from random import random
from spade.agent import Agent

from Utils.Prints import print_c
from interface import logs_color

from Agents.Airport.Behaviors.AirportRecv import RecvRequests


class Airport(Agent):

    def __init__(self, jid, password, location):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto

    def print(self, msg, color = "black"):
        print_c(f"{self.name}: {msg}", color)
        logs_color(f"{self.name}: {msg}", color)
    
    async def setup(self) -> None:
        self.print(f'Airport agent {self.location} starting...')

        # b = ReceiveFlightsBehav()
        b = RecvRequests()
        self.add_behaviour(b)

    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location
    