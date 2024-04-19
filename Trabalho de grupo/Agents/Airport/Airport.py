from random import random
from spade.agent import Agent
from Agents.Airport.Behaviors.ReceiveFlightsBehav import ReceiveFlightsBehav
from Agents.Airport.Behaviors.RecvRequests import RecvRequests
class Airport(Agent):

    def __init__(self, jid, password, location, runways=1):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto
        self.runways = runways # Pistas de deslocagem/aterragem
    
    async def setup(self) -> None:
        print(f'Airport agent {self.location} starting...')

        # b = ReceiveFlightsBehav()
        b = RecvRequests()
        self.add_behaviour(b)