import time
import tkinter as tk

import random


UPDATE_TIMER = 1



AIRPORT_PLANES = {"Lisboa": [3,5], "Porto": [3,5], "Faro": [3,5]} # {localizacao: [num_planes, hangar_capacity]} #! Tem de se meter aqui a runway_capacity
AIRPORT_LOCATIONS = list(AIRPORT_PLANES.keys())
INTERVAL = 5
NUM_OF_FLIGHTS_PER_INTERVAL = 2

class Central():
    def __init__(self, airport_locations, num_of_flights_per_interval, interval):
        self.airport_locations = airport_locations
        self.num_of_flights_per_interval = num_of_flights_per_interval
        self.interval = interval

        self.airport_label = None
        self.flights_label = None
        self.interval_label = None

    def change_random(self):
        self.num_of_flights_per_interval = random.randint(1,10)
        self.interval = random.randint(1,10)

    def display(self, root):
        label = tk.Label(root, text="Central")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        airport_locations = f"Airport Locations: {str(self.airport_locations)}"
        self.airport_label = tk.Label(frame, text=airport_locations)
        self.airport_label.grid(column=0, row=0, padx=5, pady=5)

        num_of_flights_per_interval = f"Number of flights per interval: {str(self.num_of_flights_per_interval)}"
        self.flights_label = tk.Label(frame, text=num_of_flights_per_interval)
        self.flights_label.grid(column=0, row=1, padx=5, pady=5)

        interval_value = f"Inverval: {str(self.interval)}"
        self.interval_label = tk.Label(frame, text=interval_value)
        self.interval_label.grid(column=0, row=2, padx=5, pady=5)

    def update_display(self):
        self.airport_label.config(text=f"Airport Locations: {str(self.airport_locations)}")
        self.flights_label.config(text=f"Number of flights per interval: {str(self.num_of_flights_per_interval)}")
        self.interval_label.config(text=f"Inverval: {str(self.interval)}")

    
class Airport():
    def __init__(self, location, runways=1):
        self.location = location
        self.runways = runways
        self.flights_queue = []

    def change_random(self):
        self.runways = random.randint(1, 10)
        self.location = random.choince(["Lisboa", "Porto", "Faro"])

    


class GUI():
    def __init__(self, agents):
        self.root = tk.Tk()
        self.agents = agents
        self.central = None
        self.airports = []
        self.controltowers = []
        self.hangars = []
        self.planes = []

        self.root.title("Agentes")
        self.root.geometry("500x500")


        for agent in agents:
            if agent.__class__.__name__ == "Central":
                self.central = agent
            elif agent.__class__.__name__ == "Airport":
                self.airports.append(agent)
            elif agent.__class__.__name__ == "ControlTower":
                self.controltowers.append(agent)
            elif agent.__class__.__name__ == "Hangar":
                self.hangars.append(agent)
            elif agent.__class__.__name__ == "Plane":
                self.planes.append(agent)

        self.central.display(self.root)
        self.update_loop()

    # def updateInterface(self):
    #     self.display_central(self.central)
    #     self.display_aiports(self.airports)
    #     self.display_controltowers(self.controltowers)
    #     self.display_hangars(self.hangars)
    #     self.display_planes(self.planes)

    def update_loop(self):
        self.central.update_display()
        self.central.change_random()
        self.root.after(1000, self.update_loop)
        
    
    def display_central(self, central):
        label = tk.Label(self.root, text="Central")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        airport_locations = f"Airport Locations: {str(central.airport_locations)}"
        airports = tk.Label(frame, text=airport_locations).grid(column=0, row=0, padx=5, pady=5)

        num_of_flights_per_interval = f"Number of flights per interval: {str(central.num_of_flights_per_interval)}"
        flights = tk.Label(frame, text=num_of_flights_per_interval).grid(column=0, row=1, padx=5, pady=5)

        interval_value = f"Inverval: {str(central.interval)}"
        interval = tk.Label(frame, text=interval_value).grid(column=0, row=2, padx=5, pady=5)


    def display_aiports(self, airports):
        for i, airport in enumerate(airports):
            label = tk.Label(self.root, text=f"Aeroporto {i}", font=("Arial", 12))
            label.pack(padx=10, pady=10)

            frame = tk.Frame(self.root)
            frame.pack(padx=10, pady=10)

            location = tk.Label(frame, text=f"Airport Location: {airport.location}").grid(column=0, row=0)
            runways = tk.Label(frame, text=f"Runways: {airport.runways}").grid(column=0, row=1)




    def display_controltowers(self, controltowers):
        pass


    def display_hangars(self, hangars):
        pass


    def display_planes(self, planes):
        pass








if __name__ == "__main__":
    c = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    a = Airport("Lisboa")
    gui = GUI([c, a])
    gui.root.mainloop()
