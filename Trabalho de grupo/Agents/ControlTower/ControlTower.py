from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
from Agents.ControlTower.Behaviours.DispatchPlanes import DispatchPlanes

import tkinter as tk


class ControlTower(Agent):
    # SUNNY = 0
    # RAINY = 1
    # STORMY = 2

    def __init__(self, jid, password, location, runways=4):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways_capacity = runways # Pistas de descolagem/aterragem
        self.runways_available = runways # Pistas disponíveis
        self.queue_takeoffs = []
        self.queue_landings = []
        #! WIP
        # self.weather = ControlTower.SUNNY

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

    def add_to_takeoff_queue(self, plane_jid, trip): 
        self.queue_takeoffs.append((plane_jid, trip))
        self.add_behaviour(DispatchPlanes())

    def add_to_landing_queue(self, plane_jid, trip): 
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
        
    def takeoff_queue_empty(self):
        return len(self.queue_takeoffs) == 0
    
    def landing_queue_empty(self):
        return len(self.queue_landings) == 0
        
    #> GUI methods
    # Abstract method implementation
    def create_display(self, root):
        label = tk.Label(root, text=f"Control Tower {self.location}")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        # runways = f"Runways: {str(self.runways_available)}/{str(self.runways_capacity)}"
        runways = self.present_runways()
        runways_label = tk.Label(frame, text=runways)
        runways_label.grid(column=0, row=0, padx=5, pady=5)

        # queue_takeoffs = f"Queue take-offs: {str(self.queue_takeoffs)}"
        queue_takeoffs = self.present_queue_takeoffs()
        queue_takeoffs_label = tk.Label(frame, text=queue_takeoffs)
        queue_takeoffs_label.grid(column=0, row=1, padx=5, pady=5)
        
        # queue_landings = f"Queue landings: {str(self.queue_landings)}"
        queue_landings = self.present_queue_landings()
        queue_landings_label = tk.Label(frame, text=queue_landings)
        queue_landings_label.grid(column=0, row=2, padx=5, pady=5)

        return self.CTLabels(runways_label, queue_takeoffs_label, queue_landings_label)
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        # labels_obj.runways_label.config(text=f"Runways: {str(self.runways_available)}/{str(self.runways_capacity)}")
        # labels_obj.queue_takeoffs_label.config(text=f"Queue take-offs: {str(self.queue_takeoffs)}")
        # labels_obj.queue_landings_label.config(text=f"Queue landings: {str(self.queue_landings)}")
        labels_obj.runways_label.config(text=self.present_runways())
        labels_obj.queue_takeoffs_label.config(text=self.present_queue_takeoffs())
        labels_obj.queue_landings_label.config(text=self.present_queue_landings())

    # Tem o texto que é para ser apresentado de forma modular
    def present_runways(self) -> str:
        return f"Runways: {str(self.runways_available)}/{str(self.runways_capacity)}"
    
    def present_queue_takeoffs(self) -> str:
        return f"Queue take-offs: {str(self.queue_takeoffs)}"
    
    def present_queue_landings(self) -> str:
        return f"Queue landings: {str(self.queue_landings)}"
    
    class CTLabels():
        def __init__(self, runways_label, queue_takeoffs_label, queue_landings_label):
            self.runways_label = runways_label
            self.queue_takeoffs_label = queue_takeoffs_label
            self.queue_landings_label = queue_landings_label

        