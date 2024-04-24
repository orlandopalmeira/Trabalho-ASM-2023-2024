import tkinter as tk
from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
from Agents.ControlTower.Behaviours.DispatchPlanes import DispatchPlanes

from Classes.Trip import Trip
from Config import Config as cfg

class ControlTower(Agent):
    # SUNNY = 0
    # RAINY = 1
    # STORMY = 2

    def __init__(self, jid, password, location, runways, hangar_availability):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways_capacity = runways # Pistas de descolagem/aterragem
        self.runways_available = runways # Pistas disponíveis
        self.queue_takeoffs = []
        self.queue_landings = []

        self.hangar_availability = hangar_availability #! WIP
        
        # self.weather = ControlTower.SUNNY # TODO

    async def setup(self) -> None:
        print(f'{self.name} starting...')
        self.add_behaviour(RecvRequests())

    # def set_weather(self, weather): # TODO
    #     #! Chamar self.add_behaviour(DispatchPlanes()) quando virar bom tempo
    #     self.weather = weather

    # def get_weather(self): # TODO
    #     return self.weather
    
    def get_location(self):
        return self.location
    
    
    def release_runway(self):
        self.runways_available += 1
        # Se não havia runways disponíveis, os aviões potencialmente à espera podem ser despachados
        if self.runways_available == 1:
            self.add_behaviour(DispatchPlanes()) 

    def reserve_runway_for_landing(self):
        """Reserve a runway for a plane to take off. Returns False if no hangars or runways are available, and if meteo conditions are bad."""
        if self.runways_available > 0 and self.hangar_availability > 0: #! e mais (trazer info de meteorologia)
            self.runways_available -= 1
            return True
        else:
            return False
        
    def reserve_runway_for_takeoff(self):
        """Reserve a runway for a plane to take off. Returns False if no hangars or runways are available, and if meteo conditions are bad."""
        if self.runways_available > 0: #! e mais (trazer info de meteorologia)
            self.runways_available -= 1
            return True
        else:
            return False

    def add_to_takeoff_queue(self, plane_jid: str, trip: Trip): #! Ver melhor se não seria melhor apenas armazenar o plane_jid e fazer com que o hangar já envie ao avião a sua trip a realizar.
        self.queue_takeoffs.append((plane_jid, trip))
        self.add_behaviour(DispatchPlanes())

    def add_to_landing_queue(self, plane_jid: str): 
        self.queue_landings.append(plane_jid)
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
    
    def set_hangar_availability(self, hangar_availability):
        self.hangar_availability = hangar_availability

    def increase_hangar_availability(self):
        self.hangar_availability += 1
        if self.hangar_availability == 1:
            self.add_behaviour(DispatchPlanes())

    def decrease_hangar_availability(self):
        self.hangar_availability -= 1


    #> GUI methods
    # Abstract method implementation
    def create_display(self, element):
        main_frame = tk.Frame(element.scrollable_frame, highlightbackground="black", highlightthickness=2)
        main_frame.pack(padx=5, pady=5)

        label = tk.Label(main_frame, text=f"Control Tower {self.location}", font='Arial 12 bold', fg="black")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(main_frame)
        frame.pack(padx=10, pady=10)

        #> Nota: As rows vão em numeros impares 
        row = 0
        tk.Label(frame, text="Runways: ", font='Arial 10 bold').grid(column=0, row=row)
        runways = self.present_runways()
        runways_label = tk.Label(frame, text=runways)
        runways_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        tk.Label(frame, text="Hangar availability: ", font='Arial 10 bold').grid(column=0, row=row)
        hangar_availability = self.present_hangar_availability()
        hangar_availability_label = tk.Label(frame, text=hangar_availability)
        hangar_availability_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        tk.Label(frame, text="Queue take-offs: ", font='Arial 10 bold').grid(column=0, row=row)
        queue_takeoffs = self.present_queue_takeoffs()
        queue_takeoffs_label = tk.Label(frame, text=queue_takeoffs)
        queue_takeoffs_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2
        
        tk.Label(frame, text="Queue landings: ", font='Arial 10 bold').grid(column=0, row=row)
        queue_landings = self.present_queue_landings()
        queue_landings_label = tk.Label(frame, text=queue_landings)
        queue_landings_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        return self.CTLabels(runways_label, hangar_availability_label, queue_takeoffs_label, queue_landings_label)
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        # labels_obj.runways_label.config(text=f"Runways: {str(self.runways_available)}/{str(self.runways_capacity)}")
        # labels_obj.queue_takeoffs_label.config(text=f"Queue take-offs: {str(self.queue_takeoffs)}")
        # labels_obj.queue_landings_label.config(text=f"Queue landings: {str(self.queue_landings)}")
        labels_obj.runways_label.config(text=self.present_runways())
        labels_obj.hangar_availability_label.config(text=self.present_hangar_availability())
        labels_obj.queue_takeoffs_label.config(text=self.present_queue_takeoffs())
        labels_obj.queue_landings_label.config(text=self.present_queue_landings())

    # Tem o texto que é para ser apresentado de forma modular
    def present_runways(self) -> str:
        return f"{str(self.runways_available)}/{str(self.runways_capacity)}"
    
    def present_hangar_availability(self) -> str:
        return f"{str(self.hangar_availability)}"
    
    def present_queue_takeoffs(self) -> str:
        if len(self.queue_landings) == 0:
            return "No planes waiting to take off"
        final_str = ""
        for plane_jid, trip in self.queue_takeoffs:
            final_str += f"{cfg.get_jid_name(plane_jid)} -> {trip}\n"
        return f"{final_str}"
    
    def present_queue_landings(self) -> str:
        if len(self.queue_landings) == 0:
            return "No planes waiting to land"
        final_str = ""
        for plane_jid in self.queue_landings:
            final_str += f"{cfg.get_jid_name(plane_jid)}\n"
        return f"{final_str}"
    
    class CTLabels():
        def __init__(self, runways_label, hangar_availability_label, queue_takeoffs_label, queue_landings_label):
            self.runways_label = runways_label
            self.hangar_availability_label = hangar_availability_label
            self.queue_takeoffs_label = queue_takeoffs_label
            self.queue_landings_label = queue_landings_label

        