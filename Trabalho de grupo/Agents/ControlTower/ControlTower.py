from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
from Agents.ControlTower.Behaviours.DispatchPlanes import DispatchPlanes


class ControlTower(Agent):
    # SUNNY = 0
    # RAINY = 1
    # STORMY = 2

    def __init__(self, jid, password, location, runways=4):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways_capacity = runways # Pistas de descolagem/aterragem
        self.runways_available = runways # Pistas disponíveis
        #! WIP
        # self.weather = ControlTower.SUNNY
        self.queue_takeoffs = []
        self.queue_landings = []

    async def setup(self) -> None:
        print(f'{self.name} starting...')
        self.add_behaviour(RecvRequests())

    # def set_weather(self, weather):
    #     #! Chamar self.add_behaviour(DispatchPlanes()) quando virar bom tempo
    #     self.weather = weather

    # def get_weather(self):
    #     return self.weather
    
    def get_location(self):
        return self.location
    
    
    def release_runway(self):
        self.runways_available += 1
        # Se não havia runways disponíveis, os aviões potencialmente à espera podem ser despachados
        if self.runways_available == 1:
            self.add_behaviour(DispatchPlanes()) 

    def reserve_runway(self):
        """Reserve a runway for a plane to take off. Returns False if """
        if self.runways_available > 0: #! e mais (trazer info de hangares e meteorologia)
            self.runways_available -= 1
            return True
        else:
            return False

    def add_to_takeoff_queue(self, plane_jid, trip): #! WIP
        self.queue_takeoffs.append((plane_jid, trip))
        self.add_behaviour(DispatchPlanes())

    def add_to_landing_queue(self, plane_jid, trip): #! WIP
        self.queue_landings.append((plane_jid, trip))
        self.add_behaviour(DispatchPlanes())

    def pop_from_takeoff_queue(self):
        """Retorna o primeiro elemento da fila de descolagens. Retorna None se a fila estiver vazia."""
        try:
            return self.queue_takeoffs.pop(0)
        except IndexError:
            return None
    
    def pop_from_landing_queue(self):
        """Retorna o primeiro elemento da fila de aterragens. Retorna None se a fila estiver vazia."""
        try:
            return self.queue_landings.pop(0)
        except IndexError:
            return None