from random import random
from spade.agent import Agent
import asyncio
from Config import Config as cfg
from Classes.Trip import Trip

import tkinter as tk
from tkinter import ttk

from Agents.Plane.Behaviors.PlaneRecv import RecvRequests

class Plane(Agent):
    LANDED = 0
    FLYING = 1
    CONVERSION_KM_TO_SECS = 0.01 # 1 km = 0.01 sec
    LANDING_TIME = 1 # Tempo de aterragem
    TAKEOFF_TIME = 1 # Tempo de descolagem
    
    async def setup(self) -> None:
        self.trip = None
        self.percentage_complete = 0 # Percentagem da viagem que já foi completada
        self.status = Plane.LANDED
        # self.tempo = 0 # Talvez para indicar quanto tempo a viagem demorará, mas talvez apenas seja utilizado num behaviour
        # self.carga = 0 # Talvez carga possa ser um atributo extra interessante para haver decisoes de prioridade
        print(f'{self.name} starting...')
        
        b = RecvRequests()
        self.add_behaviour(b)

    def set_trip(self, trip):
        self.trip = trip

    def set_flying(self):
        self.status = Plane.FLYING

    def set_landed(self):
        self.status = Plane.LANDED

    def get_trip(self):
        return self.trip
    
    # Usado para identificar a CT à qual tem de mandar a mensagem de descolagem
    def get_location(self):
        return self.trip.get_origin()
    
    def get_status(self):
        return self.status
    
    def __str__ (self):
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return f"{self.name}"
    

    #> GUI methods
    # Abstract method implementation
    def create_display(self, element):
        main_frame = tk.Frame(element.scrollable_frame, width=100, height=100, highlightbackground="black", highlightthickness=2)
        main_frame.pack(padx=5, pady=5)

        label = tk.Label(main_frame, text=f"Plane {self.name}")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(main_frame)
        frame.pack(padx=10, pady=10)

        trip = self.present_trip()
        trip_label = tk.Label(frame, text=trip)
        trip_label.grid(column=0, row=0, padx=5, pady=5)

        percentage_complete = self.present_percentage_complete()
        percentage_complete_label = tk.Label(frame, text=percentage_complete)
        percentage_complete_label.grid(column=0, row=1, padx=5, pady=5)
        
        status = self.present_status()
        status_label = tk.Label(frame, text=status)
        status_label.grid(column=0, row=2, padx=5, pady=5)

        return self.PLabels(trip_label, percentage_complete_label, status_label)
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        labels_obj.trip_label.config(text=self.present_trip())
        labels_obj.percentage_complete_label.config(text=self.present_percentage_complete())
        labels_obj.status_label.config(text=self.present_status())

    # Tem o texto que é para ser apresentado de forma modular
    def present_trip(self) -> str:
        return f"Trip: {str(self.trip)}"
    
    def present_percentage_complete(self) -> str:
        return f"Percentage complete: {str(self.percentage_complete)}"
    
    def present_status(self) -> str:
        if self.status == 0:
            str = "Landed"
        elif self.status == 1:
            str = "Flying"
        else:
            str = "Erro"
        return f"Status: {str}"
    
    class PLabels():
        def __init__(self, trip_label, percentage_complete_label, status_label):
            self.trip_label = trip_label
            self.percentage_complete_label = percentage_complete_label
            self.status_label = status_label
