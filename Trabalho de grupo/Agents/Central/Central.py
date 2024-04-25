from spade.agent import Agent
from random import random
from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav

class Central(Agent):

    def __init__(self, jid, password, airport_locations, num_of_flights_per_interval, interval, flights = None):
        super().__init__(jid, password)
        # Constant variables
        self.airport_locations = airport_locations
        self.num_of_flights_per_interval = num_of_flights_per_interval
        self.interval = interval
        self.historic_max_size = 10
        self.repeat_flight_plan = True if flights["repeat"] == True else False # Para o caso de ser None, ir a False

        # Auxs
        plan = flights["plan"]
        self.flight_plan = [(p["origin"], p["destination"]) for p in plan for _ in range(p["reps"])] # [(origin, destination), ...]
        self.flight_plan_index = 0

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


    #> GUI

    def present_historic(self) -> str:
        final_str = ""
        for trip in self.historic:
            final_str += f"- {trip}\n"
        return final_str
    
    def present_scarse_hangars(self) -> str:
        final_str = ""
        for hangar in self.scarse_hangars:
            final_str += f"- {hangar}\n"
        return final_str
    
    def present_crowded_hangars(self) -> str:
        final_str = ""
        for hangar in self.crowded_hangars:
            final_str += f"- {hangar}\n"
        return final_str

    
