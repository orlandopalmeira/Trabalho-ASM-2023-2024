import tkinter as tk
import time
import threading
import random
import sys

UPDATE_TIMER = 1


AIRPORT_PLANES = {"Lisboa": [3,5], "Porto": [3,5], "Faro": [3,5]} # {localizacao: [num_planes, hangar_capacity]} #! Tem de se meter aqui a runway_capacity
AIRPORT_LOCATIONS = list(AIRPORT_PLANES.keys())
INTERVAL = 5
NUM_OF_FLIGHTS_PER_INTERVAL = 2

class Central():
    def __init__(self, airport_locations, num_of_flights_per_interval, interval):
        self.name = "Central"
        self.airport_locations = airport_locations
        self.num_of_flights_per_interval = num_of_flights_per_interval
        self.interval = interval

    def change_random(self):
        self.num_of_flights_per_interval = random.randint(1,10)
        self.interval = random.randint(1,10)


    def create_display(self, root):
        label = tk.Label(root, text="Central")
        label.pack(padx=5, pady=5)

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        airport_locations = f"Airport Locations: {str(self.airport_locations)}"
        airport_label = tk.Label(frame, text=airport_locations)
        airport_label.grid(column=0, row=0, padx=5, pady=5)

        num_of_flights_per_interval = f"Number of flights per interval: {str(self.num_of_flights_per_interval)}"
        flights_label = tk.Label(frame, text=num_of_flights_per_interval)
        flights_label.grid(column=0, row=1, padx=5, pady=5)

        interval_value = f"Interval: {str(self.interval)}"
        interval_label = tk.Label(frame, text=interval_value)
        interval_label.grid(column=0, row=2, padx=5, pady=5)

        return self.CentralLabels(airport_label, flights_label, interval_label)

    def update_display(self, labels_obj):
        labels_obj.airport_label.config(text=f"Airport Locations: {str(self.airport_locations)}")
        labels_obj.flights_label.config(text=f"Number of flights per interval: {str(self.num_of_flights_per_interval)}")
        labels_obj.interval_label.config(text=f"Inverval: {str(self.interval)}")

    class CentralLabels():
        def __init__(self, airport_label, flights_label, interval_label):
            self.airport_label = airport_label
            self.flights_label = flights_label
            self.interval_label = interval_label

        

    
class Airport():
    def __init__(self, location, runways=1):
        self.name = "Airport0"
        self.location = location
        self.runways = runways
        self.flights_queue = []

    def change_random(self):
        self.runways = random.randint(1, 10)
        self.location = random.choice(["Lisboa", "Porto", "Faro"])



class GUI():
    def __init__(self, agents):
        self.root = tk.Tk()

        self.agents = agents
        self.agent_labels = []

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

        #* Creating displays for all the agents
        #TODO - terminar de implementar os métodos create_display e update_display nos restantes agentes
        # Airports
        # for a in self.airports:
        #     labels = a.create_display(self.root)
        #     self.agent_labels.append(labels)

        # ControlTowers
        for ct in self.controltowers:
            labels = ct.create_display(self.root)
            self.agent_labels.append(labels)

        for h in self.hangars:
            labels = h.create_display(self.root)
            self.agent_labels.append(labels)

        #TODO - resto dos agentes

        self.update_loop()

    def update_loop(self):
        #TODO
        # for i, a in enumerate(self.airports):
        #     a.update_display(self.agent_labels[i])

        for i, ct in enumerate(self.controltowers):
            ct.update_display(self.agent_labels[i])

        for i, h in enumerate(self.hangars):
            h.update_display(self.agent_labels[i])

        #TODO - resto dos agentes
        
        self.root.after(1000, self.update_loop)
        
list_agents = []    

def changes():
    global list_agents
    while not stop:
        time.sleep(1)
        for a in list_agents:
            a.change_random()



if __name__ == "__main__":
    c  = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    c2 = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    c3 = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    # a = Airport("Lisboa")
    list_agents = [c, c2, c3]

    stop = False
    t = threading.Thread(target=changes)
    t.start()

    gui = GUI(list_agents)
    gui.root.mainloop()
    
    stop = True
    print("Acabou!")
