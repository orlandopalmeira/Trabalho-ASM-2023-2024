from random import random
from spade.agent import Agent

from Config import Config as cfg
from Classes.Trip import Trip
from interface import logs_color
from Utils.Prints import print_c
import time

import tkinter as tk
from tkinter import ttk

from Agents.Plane.Behaviors.PlaneRecv import RecvRequests

class Plane(Agent):
    LANDED = 0
    FLYING = 1
    WAITING_LANDING_PERM = 2

    CONVERSION_KM_TO_SECS = 0.015 # 1 km = 0.015 sec

    LANDING_TIME = 2 # STANDARD landing time
    TAKEOFF_TIME = 2 # STANDARD takeoff time
    WEATHER_FACTOR = {
            "Clear": 1.0,
            "Clouds": 1.3,
            "Smoke": 1.3,
            "Mist": 1.4,
            "Haze": 1.4,
            "Dust": 1.5,
            "Drizzle": 1.6,
            "Fog": 1.8,
            "Sand": 1.8,
            "Rain": 2.0,
            "Ash": 2.2,
            "Squalls": 2.3,
            "Squall": 2.3,
            "Snow": 2.5,
            "Volcanic Ash": 3.0,
            "Tornado": 3.0,
            "Thunderstorm": 3.0
        }
    
    async def setup(self) -> None:
        self.trip = None
        self.status = Plane.LANDED
        self.landing_time = Plane.LANDING_TIME
        self.takeoff_time = Plane.TAKEOFF_TIME

        self.print(f'starting...')
        
        b = RecvRequests()
        self.add_behaviour(b)

    def print(self, msg, color = "black"):
        unix_ts = time.time()
        ts = time.strftime('%H:%M:%S', time.localtime(unix_ts))
        print_c(f"({ts}) {self.name}: {msg}", color)
        logs_color(f"({ts}) {self.name}: {msg}", color)

    def set_weather_factor_in_landing(self, weather):
        factor = self.WEATHER_FACTOR.get(weather, "1.0")
        self.landing_time = Plane.LANDING_TIME * factor

    def set_weather_factor_in_takeoff(self, weather):
        factor = self.WEATHER_FACTOR.get(weather, "1.0")
        self.takeoff_time = Plane.TAKEOFF_TIME * factor

    def set_trip(self, trip):
        self.trip = trip

    def set_flying(self):
        self.status = Plane.FLYING

    def set_landed(self):
        self.status = Plane.LANDED

    def set_waiting_landing_perm(self):
        self.status = Plane.WAITING_LANDING_PERM

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
        if self.status == self.LANDED:
            str = "Landed"
        elif self.status == self.FLYING:
            str = "Flying"
        elif self.status == self.WAITING_LANDING_PERM:
            str = "Waiting for landing perm."
        else:
            str = "!! Erro !!"
        return f"{str}"
    
    class PLabels():
        def __init__(self, trip_label, status_label):
            self.trip_label = trip_label
            # self.percentage_complete_label = percentage_complete_label
            self.status_label = status_label
