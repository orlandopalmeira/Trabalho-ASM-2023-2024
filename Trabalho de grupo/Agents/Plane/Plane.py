from random import random
from spade.agent import Agent
# from Behaviors.send_request_behav import SendRequestBehav

class Plane(Agent):
    
    async def setup(self) -> None:
        self.location
        print(f'Airport agent {str(self.jid)} starting...')
        
        # a = SendRequestBehav(period=2)
        # self.add_behaviour(a)
    