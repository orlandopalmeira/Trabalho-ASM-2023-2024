from spade.agent import Agent
from random import random
from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav

class Central(Agent):

    def __init__(self, jid, password, airport_locations, num_of_flights_per_interval, interval):
        super().__init__(jid, password)
        # Constant variables
        self.airport_locations = airport_locations
        self.num_of_flights_per_interval = num_of_flights_per_interval
        self.interval = interval
        self.historic_max_size = 10

        # Variables
        self.historic = [] # Com um histórico de 10 viagens
        self.scarse_hangars = []
        self.crowded_hangars = [] 

    
    async def setup(self) -> None:
        print(f'\nCentral agent starting...')
        a = GenerateFlightsBehav(period=self.interval)
        self.add_behaviour(a)
    
    def add_to_historic(self, trip):
        if len(self.historic) == self.historic_max_size:
            self.historic.pop(0)
        self.historic.append(trip)

    def get_historic(self):
        return self.historic
    
    def add_to_scarse_hangars(self, hangar):
        self.scarse_hangars.append(hangar)

    def get_scarse_hangars(self):
        return self.scarse_hangars
    
    def add_to_crowded_hangars(self, hangar):
        self.crowded_hangars.append(hangar)

    def get_crowded_hangars(self):
        return self.crowded_hangars
    
    def remove_from_scarse_hangars(self, hangar):
        self.scarse_hangars.remove(hangar)

    def remove_from_crowded_hangars(self, hangar):
        self.crowded_hangars.remove(hangar)