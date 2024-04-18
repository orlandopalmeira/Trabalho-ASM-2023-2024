from random import random
from spade.agent import Agent
# from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav

class Plane(Agent):
    LANDED = 0
    FLYING = 1
    
    async def setup(self) -> None:
        self.origem = None
        self.destino = None
        self.percentage_complete = 0 # Percentagem da viagem que já foi completada
        self.status = Plane.LANDED
        # self.tempo = 0 # Talvez para indicar quanto tempo a viagem demorará, mas talvez apenas seja utilizado num behaviour
        # self.carga = 0 # Talvez carga possa ser um atributo extra interessante para haver decisoes de prioridade
        print(f'{self.name} starting...')
        
        # a = SendRequestBehav(period=2)
        # self.add_behaviour(a)

    def set_origin(self, location):
        self.origem = location

    def set_destination(self, location):
        self.destino = location

    def set_status(self, status):
        self.status = status

    def get_origin(self):
        return self.origem
    
    def get_destination(self):
        return self.destino
    
    def get_status(self):
        return self.status