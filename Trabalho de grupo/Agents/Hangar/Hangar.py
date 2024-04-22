from random import random
from spade.agent import Agent
# from Agents.Central.Behaviors.GenerateFlightsBehav import GenerateFlightsBehav
from Agents.Hangar.Behaviors.HangarRecv import RecvPlaneRequests

import tkinter as tk

class Hangar(Agent):
    
    def __init__(self, jid, password, location, capacity=5, planes=None):
        super().__init__(jid, password)
        self.location = location
        self.planes = [] if planes is None else planes # Lista de strings que serão os jids dos avioes
        self.capacity = capacity
        self.waiting_requests = 0

    async def setup(self):
        print(f'{self.name} starting...')
        self.add_behaviour(RecvPlaneRequests())
    

    def add_plane(self, plane_jid):
        self.planes.append(plane_jid)

    def increment_waiting_requests(self):
        self.waiting_requests += 1

    def decrement_waiting_requests(self):
        self.waiting_requests -= 1

    def pop_plane(self):
        """Caso não haja aviões disponíveis, retorna None. Caso contrário, retorna o jid do avião."""
        try:
            return self.planes.pop(0)
        except IndexError:
            return None

    def set_capacity(self, capacity):
        self.capacity = capacity


    #> GUI methods
    # Abstract method implementation
    def create_display(self, root):
        label = tk.Label(root, text=f"Hangar {self.location}")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        capacity = self.present_capacity()
        capacity_label = tk.Label(frame, text=capacity)
        capacity_label.grid(column=0, row=0, padx=5, pady=5)

        waiting_request = self.present_waiting_requests()
        waiting_request_label = tk.Label(frame, text=waiting_request)
        waiting_request_label.grid(column=0, row=1, padx=5, pady=5)
        
        planes = self.present_planes()
        planes_label = tk.Label(frame, text=planes)
        planes_label.grid(column=0, row=2, padx=5, pady=5)

        return self.HLabels(capacity_label, waiting_request_label, planes_label)
    
    # Abstract method implementation
    def update_display(self, labels_obj):
        labels_obj.capacity_label.config(text=self.present_capacity())
        labels_obj.waiting_request_label.config(text=self.present_waiting_requests())
        labels_obj.planes_label.config(text=self.present_planes())

    # Tem o texto que é para ser apresentado de forma modular
    def present_capacity(self) -> str:
        return f"Capacity: {str(self.capacity)}"
    
    def present_waiting_requests(self) -> str:
        return f"Number of waiting requests: {str(self.waiting_requests)}"
    
    def present_planes(self) -> str:
        str = "\n".join(self.planes)
        return f"Planes:\n{str}"
    
    class HLabels():
        def __init__(self, capacity_label, waiting_request_label, planes_label):
            self.capacity_label = capacity_label
            self.waiting_request_label = waiting_request_label
            self.planes_label = planes_label

        