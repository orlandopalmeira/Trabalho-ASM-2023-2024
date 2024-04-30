from random import random
from spade.agent import Agent

from Utils.Prints import *

from Agents.Airport.Behaviors.AirportRecv import RecvRequests


class Airport(Agent):

    def __init__(self, jid, password, location):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto

    def print(self, msg):
        print(f"{self.agent.name}: {msg}")
    
    async def setup(self) -> None:
        print_info(f'Airport agent {self.location} starting...')

        # b = ReceiveFlightsBehav()
        b = RecvRequests()
        self.add_behaviour(b)

    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location
    