from random import random
from spade.agent import Agent

from Config import Config as cfg
from Classes.Trip import Trip
from interface import logs_color
from Utils.Prints import print_c

import tkinter as tk
from tkinter import ttk

from Agents.Plane.Behaviors.PlaneRecv import RecvRequests

class Plane(Agent):
    LANDED = 0
    FLYING = 1
    CONVERSION_KM_TO_SECS = 0.01 # 1 km = 0.01 sec
    LANDING_TIME = 3 # Tempo de aterragem em secs
    TAKEOFF_TIME = 3 # Tempo de descolagem em secs
    
    async def setup(self) -> None:
        self.trip = None
        # self.percentage_complete = 0 # Percentagem da viagem que já foi completada
        self.status = Plane.LANDED
        # self.tempo = 0 # Talvez para indicar quanto tempo a viagem demorará, mas talvez apenas seja utilizado num behaviour
        # self.carga = 0 # Talvez carga possa ser um atributo extra interessante para haver decisoes de prioridade
        self.print(f'starting...')
        
        b = RecvRequests()
        self.add_behaviour(b)

    def print(self, msg, color = "black"):
        print_c(f"{self.name}: {msg}", color)
        logs_color(f"{self.name}: {msg}", color)

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
        main_frame = tk.Frame(element.scrollable_frame, highlightbackground="black", highlightthickness=2)
        main_frame.pack(padx=5, pady=5)

        label = tk.Label(main_frame, text=f"Plane {self.name}", font='Arial 12 bold', fg="black")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(main_frame)
        frame.pack(padx=10, pady=10)

        row = 0
        tk.Label(frame, text="Trip: ", font='Arial 10 bold').grid(column=0, row=row)
        trip = self.present_trip()
        trip_label = tk.Label(frame, text=trip)
        trip_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        # tk.Label(frame, text="Percentage complete: ", font='Arial 10 bold').grid(column=0, row=row)
        # percentage_complete = self.present_percentage_complete()
        # percentage_complete_label = tk.Label(frame, text=percentage_complete)
        # percentage_complete_label.grid(column=0, row=row+1, padx=5, pady=5)
        # row+=2
        
        tk.Label(frame, text="Status: ", font='Arial 10 bold').grid(column=0, row=row)
        status = self.present_status()
        status_label = tk.Label(frame, text=status)
        status_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        return self.PLabels(trip_label, status_label)
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        labels_obj.trip_label.config(text=self.present_trip())
        # labels_obj.percentage_complete_label.config(text=self.present_percentage_complete())
        labels_obj.status_label.config(text=self.present_status())

    # Tem o texto que é para ser apresentado de forma modular
    def present_trip(self) -> str:
        return f"{str(self.trip)}"
    
    # def present_percentage_complete(self) -> str:
    #     return f"{str(self.percentage_complete)}"
    
    def present_status(self) -> str:
        if self.status == 0:
            str = "Landed"
        elif self.status == 1:
            str = "Flying"
        else:
            str = "Erro"
        return f"{str}"
    
    class PLabels():
        def __init__(self, trip_label, status_label):
            self.trip_label = trip_label
            # self.percentage_complete_label = percentage_complete_label
            self.status_label = status_label
