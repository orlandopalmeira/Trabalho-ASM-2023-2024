from random import random
from spade.agent import Agent
# from Behaviors.ReceiveFlightsBehav import ReceiveFlightsBehav

class Hangar(Agent):
    
    def __init__(self, jid, password, location, planes=[], capacity=5):
        super().__init__(jid, password)
        self.location = location
        self.planes = planes # Lista de strings que serão os jids dos avioes
        self.capacity = capacity

    async def setup(self) -> None:
        print(f'Hangar agent {self.location} starting...')
        
        # a = SendRequestBehav(period=2)
        # self.add_behaviour(a)

