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
        self.waiting_requests = 0

    async def setup(self) -> None:
        print(f'Hangar agent {self.location} starting...')
        self.add_behaviour(RecvPlaneRequests())
    

    def add_plane(self, plane_jid):
        self.planes.append(plane_jid)

    def increment_waiting_requests(self):
        self.waiting_requests += 1

    def decrement_waiting_requests(self):
        self.waiting_requests -= 1

    def pop_plane(self):
        """Caso não haja aviões disponíveis, retorna None. Caso contrário, retorna o jid do avião."""
        try:
            return self.planes.pop(0)
        except IndexError:
            return None

    def set_capacity(self, capacity):
        self.capacity = capacity
