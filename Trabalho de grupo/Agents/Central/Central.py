from spade.agent import Agent
from spade.message import Message

from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav
from Agents.Central.Behaviors.CentralRecv import RecvRequests
from Agents.Central.Behaviors.ResolveHangars import ResolveHangars

from Classes.HangarReport import HangarReport

from Config import Config as cfg
from interface import logs_color
from Utils.Prints import print_c

import jsonpickle
import asyncio

import tkinter as tk
# from tkinter import ttk

class Central(Agent):

    # def __init__(self, jid, password, airport_locations, num_of_flights_per_interval, interval, flights = None):
    def __init__(self, jid, password, airport_locations, flights_cfg):
        super().__init__(jid, password)
        self.airport_locations = airport_locations
        self.num_of_flights_per_interval = flights_cfg.get("num_of_flights_per_interval", 1)
        self.interval = flights_cfg.get("interval", 10)

        # Auxs
        if flights_cfg.get("plan") == None:
            self.flight_plan = None
        else:
            plan = flights_cfg["plan"]
            self.flight_plan = [(p["origin"], p["destination"]) for p in plan for _ in range(p["reps"])] # [(origin, destination), ...]
            self.flight_plan_index = 0
            self.repeat_flight_plan = flights_cfg.get("repeat", False)

        self.historic_max_size = 5
        self.historic = []
        self.scarse_hangars = []
        self.crowded_hangars = [] 

    
    async def setup(self) -> None:
        self.print(f'starting...')
        recv = RecvRequests()
        resolve = ResolveHangars(period=6)
        gf = GenerateFlightsBehav(period=self.interval)
        self.add_behaviour(recv)
        self.add_behaviour(resolve)
        # await asyncio.sleep(4) #! PARA DAR TEMPO DOS OUTROS AGENTES COMEÇAREM
        self.add_behaviour(gf)

    def create_trip_msg(self, trip) -> Message:
        self.print(f"Flight generated {trip}", "blue")
        airport_name = cfg.get_airport_jid(trip.get_origin())
        msg = Message(to=airport_name, metadata={'performative':'request'}, body=jsonpickle.encode(trip))
        self.add_to_historic(trip)
        return msg
        

    def print(self, msg, color = "black"):
        print_c(f"\n{self.name}: {msg}\n", color)
        logs_color(f"\n{self.name}: {msg}\n", color)
    
    def add_to_historic(self, trip):
        if len(self.historic) == self.historic_max_size:
            self.historic.pop(0)
        self.historic.append(trip)

    def get_historic(self):
        return self.historic.copy()
    
    def get_scarse_hangars(self):
        return self.scarse_hangars.copy()
    
    def get_crowded_hangars(self):
        return self.crowded_hangars.copy()
    
    def add_to_scarse_hangars(self, hangar_rep: HangarReport):
        # Remover um pedido se já existir #! talvez fazer mensagens de remover de scrarse/crowded hangar e fazer com que esta remoção de baixo, o seu timestamp fique no novo pedido
        for hr in self.scarse_hangars:
            if hr.get_location() == hangar_rep.get_location():
                self.scarse_hangars.remove(hr)
                break
        # Insert ordenado consoante o __lt__ definido na classe HangarReport e em que os primeiros têm prioridade
        for i, hr in enumerate(self.scarse_hangars):
            if hr < hangar_rep:
                self.scarse_hangars.insert(i, hangar_rep)
                return
        self.scarse_hangars.append(hangar_rep)
    
    def add_to_crowded_hangars(self, hangar_rep: HangarReport):
        # Remover um pedido se já existir #! talvez fazer mensagens de remover de scrarse/crowded hangar
        last_ts = None
        for hr in self.crowded_hangars:
            if hr.get_location() == hangar_rep.get_location():
                self.crowded_hangars.remove(hr)
                last_ts = hr.get_timestamp()
                break
        # Um pedido ainda esteja na central, o seu timestamp antigo fique no novo pedido
        if last_ts != None:
            hangar_rep.set_timestamp(last_ts)
        # Insert ordenado consoante o __lt__ definido na classe HangarReport e em que os primeiros têm prioridade
        for i, hr in enumerate(self.crowded_hangars):
            if hr < hangar_rep:
                self.crowded_hangars.insert(i, hangar_rep)
                return
        self.crowded_hangars.append(hangar_rep)
    
    def remove_from_scarse_hangars(self, hangar_rep: HangarReport):
        for hr in self.scarse_hangars:
            if hr.get_location() == hangar_rep.get_location():
                self.scarse_hangars.remove(hr)
                return

    def remove_from_crowded_hangars(self, hangar_rep: HangarReport):
        for hr in self.crowded_hangars:
            if hr.get_location() == hangar_rep.get_location():
                self.crowded_hangars.remove(hr)
                return
            
    #> GUI
    def create_display(self, element):
        main_frame = tk.Frame(element.scrollable_frame, highlightbackground="black", highlightthickness=2)
        main_frame.pack(padx=5, pady=5)

        label = tk.Label(main_frame, text=f"Central", font='Arial 12 bold', fg="black")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(main_frame)
        frame.pack(padx=10, pady=10)

        row = 0
        tk.Label(frame, text="Historic: ", font='Arial 10 bold').grid(column=0, row=row)
        historic = self.present_historic()
        historic_label = tk.Label(frame, text=historic)
        historic_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        tk.Label(frame, text="Scarse Hangars: ", font='Arial 10 bold').grid(column=0, row=row)
        scarse_hangars = self.present_scarse_hangars()
        scarse_hangars_label = tk.Label(frame, text=scarse_hangars)
        scarse_hangars_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2
        
        tk.Label(frame, text="Crowded Hangars: ", font='Arial 10 bold').grid(column=0, row=row)
        crowded_hangars = self.present_crowded_hangars()
        crowded_hangars_label = tk.Label(frame, text=crowded_hangars)
        crowded_hangars_label.grid(column=0, row=row+1, padx=5, pady=5)
        row+=2

        return self.CLabels(historic_label, scarse_hangars_label, crowded_hangars_label)
    

    # Abstract method implementation
    def update_display(self, labels_obj):
        labels_obj.historic_label.config(text=self.present_historic())
        labels_obj.scarse_hangars_label.config(text=self.present_scarse_hangars())
        labels_obj.crowded_hangars_label.config(text=self.present_crowded_hangars())


    def present_historic(self) -> str:
        final_str = f"(Last {self.historic_max_size} flights)\n"
        for historic in self.historic:
            final_str += f"\n- {historic}"
        return final_str
    
    def present_scarse_hangars(self) -> str:
        final_str = ""
        if len(self.scarse_hangars) == 0:
            final_str = "No scarse hangars."
        for hangar in self.scarse_hangars:
            final_str += f"- {hangar}\n"
        return final_str
    
    def present_crowded_hangars(self) -> str:
        final_str = ""
        if len(self.crowded_hangars) == 0:
            final_str = "No crowded hangars."
        for hangar in self.crowded_hangars:
            final_str += f"- {hangar}\n"
        return final_str


    class CLabels():
        def __init__(self, historic_label, scarse_hangars_label, crowded_hangars_label):
            self.historic_label = historic_label
            self.scarse_hangars_label = scarse_hangars_label
            self.crowded_hangars_label = crowded_hangars_label
    
