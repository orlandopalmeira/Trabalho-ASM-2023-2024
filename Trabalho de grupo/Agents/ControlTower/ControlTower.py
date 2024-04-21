from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
# from Agents.ControlTower.Behaviours.AllowMovement import AllowMovement



class ControlTower(Agent):
    # SUNNY = 0
    # RAINY = 1
    # STORMY = 2


    def __init__(self, jid, password, location, runways=1):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways_capacity = runways # Pistas de descolagem/aterragem
        self.runways_available = runways # Pistas disponíveis
        #! WIP
        # self.weather = ControlTower.SUNNY
        # self.queue_takeoffs = []
        # self.queue_landings = []

    async def setup(self) -> None:
        print(f'ControlTower agent {self.location} starting...')
        self.add_behaviour(RecvRequests())

    # def set_weather(self, weather):
    #     self.weather = weather

    # def get_weather(self):
    #     return self.weather
    
    def get_location(self):
        return self.location
    
    
    def release_runway(self):
        self.runways_available += 1

    def reserve_runway(self):
        """Reserve a runway for a plane to take off. Returns False if """
        # if self.runways_available > 0 and self.weather != ControlTower.STORMY:
        if self.runways_available > 0:
            self.runways_available -= 1
            return True
        else:
            return False


    # def __signal_availabilty(self): #! WIP
    #     """Vai verificar se existem aviões à espera para descolar ou aterrar, após ter havido um bloqueio da CT"""
    #     self.add_behaviour(AllowMovement())