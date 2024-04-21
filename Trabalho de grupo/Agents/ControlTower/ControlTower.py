from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
class ControlTower(Agent):
    def __init__(self, jid, password, location, runways=1):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways = runways # Pistas de descolagem/aterragem

    async def setup(self) -> None:
        print(f'ControlTower agent {self.location} starting...')
        self.add_behaviour(RecvRequests())

    def add_runway(self):
        self.runways += 1

    def get_runway(self):
        if self.runways > 0:
            self.runways -= 1
            return True
        else:
            return False

