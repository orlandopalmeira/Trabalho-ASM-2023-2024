from random import random
from spade.agent import Agent
# from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav
from Agents.Hangar.Behaviors.RecvPlaneRequests import RecvPlaneRequests
class Hangar(Agent):
    
    def __init__(self, jid, password, location, capacity=5, planes=None):
        super().__init__(jid, password)
        self.location = location
        self.planes = [] if planes is None else planes # Lista de strings que serão os jids dos avioes
        self.capacity = capacity

    async def setup(self) -> None:
        print(f'Hangar agent {self.location} starting...')
        self.add_behaviour(RecvPlaneRequests())
        # a = SendRequestBehav(period=2)
        # self.add_behaviour(a)
    
    def add_plane(self, plane_jid):
        self.planes.append(plane_jid)

    def set_capacity(self, capacity):
        self.capacity = capacity
