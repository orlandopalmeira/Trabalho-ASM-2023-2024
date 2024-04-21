from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
class ControlTower(Agent):
    def __init__(self, jid, password, location, runways=1):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways_capacity = runways # Pistas de descolagem/aterragem
        self.runways_available = runways # Pistas disponíveis

    async def setup(self) -> None:
        print(f'ControlTower agent {self.location} starting...')
        self.add_behaviour(RecvRequests())

    def release_runway(self):
        self.runways_available += 1

    def reserve_runway(self):
        if self.runways_available > 0:
            self.runways_available -= 1
            return True
        else:
            return False

