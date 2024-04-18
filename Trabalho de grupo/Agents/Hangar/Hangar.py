from random import random
from spade.agent import Agent
# from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav

class Hangar(Agent):
    
    def __init__(self, jid, password, location, capacity=5, planes=[]):
        super().__init__(jid, password)
        self.location = location
        self.planes = planes # Lista de strings que serão os jids dos avioes
        self.capacity = capacity

    async def setup(self) -> None:
        print(f'Hangar agent {self.location} starting...')
        
        # a = SendRequestBehav(period=2)
        # self.add_behaviour(a)
    
    def add_plane(self, plane_jid):
        self.planes.append(plane_jid)

    def set_capacity(self, capacity):
        self.capacity = capacity
