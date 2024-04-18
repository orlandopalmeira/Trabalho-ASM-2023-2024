from random import random
from spade.agent import Agent
# from Behaviors.send_request_behav import SendRequestBehav

class Central(Agent):

    def __init__(self, jid, password, airport_locations, num_of_flights_per_interval, interval):
        super().__init__(jid, password)
        self.airport_locations = airport_locations
        self.num_of_flights_per_interval = num_of_flights_per_interval
        self.interval = interval

    
    async def setup(self) -> None:
        pass
        # a = SendRequestBehav(period=2)
        # self.add_behaviour(a)
    