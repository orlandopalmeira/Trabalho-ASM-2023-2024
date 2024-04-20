from random import random
from spade.agent import Agent
import asyncio
from Config import Config as cfg

from Agents.Plane.Behaviors.PlaneRecv import RecvRequests

class Plane(Agent):
    LANDED = 0
    FLYING = 1
    CONVERSION_KM_TO_SECS = 0.01 # 1 km = 0.01 sec
    
    async def setup(self) -> None:
        self.trip = None
        self.percentage_complete = 0 # Percentagem da viagem que já foi completada
        self.status = Plane.LANDED
        # self.tempo = 0 # Talvez para indicar quanto tempo a viagem demorará, mas talvez apenas seja utilizado num behaviour
        # self.carga = 0 # Talvez carga possa ser um atributo extra interessante para haver decisoes de prioridade
        print(f'{self.name} starting...')
        
        b = RecvRequests()
        self.add_behaviour(b)

    def set_trip(self, trip):
        self.trip = trip

    def set_flying(self):
        self.status = Plane.FLYING

    def set_landed(self):
        self.status = Plane.LANDED

    def get_trip(self):
        return self.trip
    
    def get_status(self):
        return self.status
    