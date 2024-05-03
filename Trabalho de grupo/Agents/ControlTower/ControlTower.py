import tkinter as tk
from tkinter import ttk
from Agents.Meteo.Meteo import Meteo

from spade.agent import Agent

from Agents.ControlTower.Behaviours.CTRecv import RecvRequests
from Agents.ControlTower.Behaviours.DispatchPlanes import DispatchPlanes

from Config import Config as cfg
from interface import logs_color
from Utils.Prints import print_c

from Classes.Trip import Trip
from Classes.Weather import Weather

import json
import time

GOOD_WEATHER = cfg.get_good_weather() # "Clear"
MID_WEATHER  = cfg.get_mid_weather() # "Rain"
BAD_WEATHER  = cfg.get_bad_weather() # "Thunderstorm"


class ControlTower(Agent):
    MID_CONDITIONS = ["Clouds", "Smoke", "Mist", "Haze", "Dust", "Drizzle", "Fog", "Sand", "Rain", "Ash", "Squalls", "Squall", "Snow"] # Condições que atrasam descolagens e aterragens
    BAD_CONDITIONS = ["Thunderstorm", "Tornado", "Volcanic Ash"] # Condições que impedem descolagens e aterragens

    def __init__(self, jid, password, location, runways, hangar_availability: int):
        super().__init__(jid, password)
        self.location = location # Localização (cidade) do aeroporto onde a torre está
        self.runways_capacity = runways # Pistas de descolagem/aterragem
        self.runways_available = runways # Pistas disponíveis
        self.queue_takeoffs = [] # lista de tuplos (plane_jid, trip)
        self.queue_landings = [] # lista de plane_jids

        self.hangar_availability = hangar_availability 
        
        self.weather: str = GOOD_WEATHER

    def print(self, msg, color = "black"):
        unix_ts = time.time()
        ts = time.strftime('%H:%M:%S', time.localtime(unix_ts))
        print_c(f"({ts}) {self.name}: {msg}", color)
        logs_color(f"({ts}) {self.name}: {msg}", color)

    async def setup(self) -> None:
        self.print(f'{self.name} starting...')
        self.add_behaviour(RecvRequests())

    def set_weather(self, weather):
        was_bad_weather = self.is_bad_weather(self.weather)
        self.weather = weather
        if was_bad_weather and not self.is_bad_weather(weather):
            self.add_behaviour(DispatchPlanes()) 

    def switch_weather(self):
        """For the button that switches weather manually, but with file logic"""
        meteo = cfg.meteo_file_name()
        city = self.location
        with open(meteo, 'r') as meteo_file:
            meteo_obj = json.load(meteo_file)

        if self.is_bad_weather(meteo_obj[city]):
            # self.set_weather(GOOD) #! não é preciso o set_weather, pq isto vai mudar um ficheiro que o agente METEO está a ler e vai informar sempre a CT desse valor. E ao receber esse valor do METEO, é que se vai executar o set_weather
            meteo_obj[city] = GOOD_WEATHER
        
        elif self.is_mid_weather(meteo_obj[city]):
            # self.set_weather(BAD)
            meteo_obj[city] = BAD_WEATHER
        else:
            # self.set_weather(MID)
            meteo_obj[city] = MID_WEATHER
        
        with open(meteo, 'w') as meteo_file:
            json.dump(meteo_obj, meteo_file, indent=4)


    
    def get_location(self):
        return self.location
    
    def get_weather(self) -> Weather:
        res = Weather(self.weather)
        return res
    
    
    def release_runway(self):
        self.runways_available += 1
        # Se não havia runways disponíveis, os aviões potencialmente à espera podem ser despachados
        if self.runways_available == 1:
            self.add_behaviour(DispatchPlanes()) 

    def reserve_runway_for_landing(self):
        """Reserve a runway for a plane to take off. Returns False if no hangars or runways are available, and if meteo conditions are bad."""
        if self.runways_available > 0 and self.hangar_availability > 0 and not self.is_bad_weather(self.weather): #! Condições de movimentação de aviões
            self.runways_available -= 1
            return True
        else:
            return False
        
    def reserve_runway_for_takeoff(self):
        """Reserve a runway for a plane to take off. Returns False if no hangars or runways are available, and if meteo conditions are bad."""
        if self.runways_available > 0 and not self.is_bad_weather(self.weather): #! Condições de movimentação de aviões
            self.runways_available -= 1
            return True
        else:
            return False

    def add_to_takeoff_queue(self, plane_jid: str, trip: Trip):
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

    #* Weather qualifiers
    def is_bad_weather(self, weather) -> bool:
        """Checks if weather conditions prevents takeoffs and landings."""
        very_bad_conditions = self.BAD_CONDITIONS
        return weather in very_bad_conditions
    
    def is_mid_weather(self, weather) -> bool:
        """Checks if weather conditions slows down takeoffs and landings."""
        mid_conditions = self.MID_CONDITIONS
        return weather in mid_conditions
    
    def is_good_weather(self, weather) -> bool:
        """Checks if weather conditions are optimal for takeoffs and landings."""
        return not self.is_mid_weather(weather) and not self.is_bad_weather(weather)
    


    #> GUI methods
    # Abstract method implementation
    def create_display(self, element, meteo_mode):
        main_frame = tk.Frame(element.scrollable_frame, highlightbackground="black", highlightthickness=2)
        main_frame.pack(padx=5, pady=5)

        label = tk.Label(main_frame, text=f"Control Tower {self.location}", font='Arial 12 bold', fg="black")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(main_frame)
        frame.pack(padx=10, pady=10)

        #> Nota: As rows vão em numeros impares 
        row = 0
        tk.Label(frame, text="Runways available: ", font='Arial 10 bold').grid(column=0, row=row)
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

        tk.Label(frame, text="Weather: ", font='Arial 10 bold').grid(column=0, row=row)
        weather = self.present_weather()
        weather_label = tk.Label(frame, text=weather)
        weather_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        if meteo_mode == Meteo.MODE_MANUAL:
            button = ttk.Button(frame, text="Change Weather", command=self.switch_weather)
            button.grid(column=0, row=row, padx=5, pady=5)
            row+=1

        return self.CTLabels(runways_label, hangar_availability_label, queue_takeoffs_label, queue_landings_label, weather_label)
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        labels_obj.runways_label.config(text=self.present_runways())
        labels_obj.hangar_availability_label.config(text=self.present_hangar_availability())
        labels_obj.queue_takeoffs_label.config(text=self.present_queue_takeoffs())
        labels_obj.queue_landings_label.config(text=self.present_queue_landings())
        labels_obj.weather_label.config(text=self.present_weather())

    # Tem o texto que é para ser apresentado de forma modular
    def present_weather(self) -> str:
        if self.is_bad_weather(self.weather):
            return f"{self.weather} (bad)"
        return f"{self.weather}"

    def present_runways(self) -> str:
        return f"{str(self.runways_available)}/{str(self.runways_capacity)}"
    
    def present_hangar_availability(self) -> str:
        return f"{str(self.hangar_availability)}"
    
    def present_queue_takeoffs(self) -> str:
        if len(self.queue_takeoffs) == 0:
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
        def __init__(self, runways_label, hangar_availability_label, queue_takeoffs_label, queue_landings_label, weather_label):
            self.runways_label = runways_label
            self.hangar_availability_label = hangar_availability_label
            self.queue_takeoffs_label = queue_takeoffs_label
            self.queue_landings_label = queue_landings_label
            self.weather_label = weather_label

        