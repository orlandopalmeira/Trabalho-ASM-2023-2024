from random import random
from spade.agent import Agent

from Agents.Hangar.Behaviors.HangarRecv import RecvPlaneRequests

from Config import Config as cfg
from Utils.Prints import *

import tkinter as tk

class Hangar(Agent):
    
    def __init__(self, jid, password, location, capacity, planes=None):
        super().__init__(jid, password)
        self.location = location
        self.planes = [] if planes is None else planes # Lista de strings que serão os jids dos avioes
        self.capacity = capacity
        self.waiting_requests = [] # TODO: Implementar a lista de trips que ainda não foram atendidas (talvez implementar estratégia similar à dispatch planes)

    def print(self, msg):
        print(f"{self.name}: {msg}")

    async def setup(self):
        print(f'{self.name} starting...')
        self.add_behaviour(RecvPlaneRequests())
    

    def add_plane(self, plane_jid):
        plane_jid_str = str(plane_jid)
        # Error detection
        if plane_jid_str in self.planes:
            self.print(red_text(f"Plane {plane_jid_str} already in hangar {self.location}"))
        if len(self.planes) == self.capacity:
            self.print(red_text(f"Plane {plane_jid_str} could not be added to hangar {self.location} due to lack of space"))
            # return
        # Functionality
        self.planes.append(plane_jid_str)
        


    
    def pop_plane(self):
        """Caso não haja aviões disponíveis, retorna None. Caso contrário, retorna o jid do avião."""
        try:
            return self.planes.pop(0)
        except IndexError:
            return None

    def pop_waiting_requests(self):
        try:
            return self.waiting_requests.pop()
        except IndexError:
            return None

    def add_waiting_request(self, trip):
        self.waiting_requests.append(trip)

    def set_capacity(self, capacity):
        self.capacity = capacity


    #> GUI methods
    # Abstract method implementation
    def create_display(self, element):
        main_frame = tk.Frame(element, highlightbackground="black", highlightthickness=2)
        main_frame.pack(padx=5, pady=5)

        label = tk.Label(main_frame, text=f"Hangar {self.location}", font='Arial 12 bold', fg="black")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(main_frame)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Capacity: ", font='Arial 8 bold').grid(column=0, row=0)
        capacity = self.present_capacity()
        capacity_label = tk.Label(frame, text=capacity)
        capacity_label.grid(column=0, row=1, padx=5, pady=5)

        # tk.Label(frame, text="Waiting requests: ", font='Arial 8 bold').grid(column=0, row=2)
        # waiting_request = self.present_waiting_requests()
        # waiting_request_label = tk.Label(frame, text=waiting_request)
        # waiting_request_label.grid(column=0, row=3, padx=5, pady=5)
        
        tk.Label(frame, text="Planes: ", font='Arial 8 bold').grid(column=0, row=4)
        planes = self.present_planes()
        planes_label = tk.Label(frame, text=planes)
        planes_label.grid(column=0, row=3, padx=5, pady=5)

        return self.HLabels(capacity_label, 
                            # waiting_request_label, 
                            planes_label
                            )
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        labels_obj.capacity_label.config(text=self.present_capacity())
        # labels_obj.waiting_request_label.config(text=self.present_waiting_requests())
        labels_obj.planes_label.config(text=self.present_planes())

    # Tem o texto que é para ser apresentado de forma modular
    def present_capacity(self) -> str:
        return f"{len(self.planes)}/{str(self.capacity)}"
    
    def present_waiting_requests(self) -> str:
        str_final = "\n".join(self.waiting_requests)
        return f"{str_final}"

    def present_planes(self) -> str:
        str_final = "\n".join(self.planes)
        return f"{cfg.get_jid_name(str_final)}"
    
    class HLabels():
        def __init__(self, 
                     capacity_label,
                    #  waiting_request_label,
                     planes_label
                     ):
            self.capacity_label = capacity_label
            # self.waiting_request_label = waiting_request_label
            self.planes_label = planes_label

        