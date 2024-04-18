from random import random
from spade.agent import Agent
from Agents.Airport.Behaviors.ReceiveFlightsBehav import ReceiveFlightsBehav

class Airport(Agent):

    def __init__(self, jid, password, location):
        super().__init__(jid, password)
        self.location = location
    
    async def setup(self) -> None:
        print(f'Airport agent {self.location} starting...')

        b = ReceiveFlightsBehav()
        self.add_behaviour(b)
        