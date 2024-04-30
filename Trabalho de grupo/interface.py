import tkinter as tk
import time
import threading
import random
import sys
from tkinter import ttk

# UPDATE_TIMER = 1
LOGS = []

# Função geral
def logs_color(text, color):
    LOGS.insert(0, (text, color)) #! Não se pode fazer isto pq ao meter na dashboard, o novo conteudo é metido em baixo e assim ficariam secções no sentido baixo->cima, mas 
    # LOGS.append((text, color)) 


class GUI():
    def __init__(self, agents):
        self.root = tk.Tk()

        self.agents = agents

        self.airports = []
        self.airport_labels = []

        col_pointer = 0

        self.central = []
        self.central_labels = []
        self.central_frame = ScrollableFrame(self.root, width=200, height=800, relief=tk.RAISED, borderwidth=2)
        self.central_frame.grid(column=col_pointer, row=0, padx=5, pady=5)
        col_pointer += 1

        self.hangars = []
        self.hangar_labels = []
        self.hangar_frame = ScrollableFrame(self.root, width=180, height=800, relief=tk.RAISED, borderwidth=2)
        self.hangar_frame.grid(column=col_pointer, row=0, padx=5, pady=5)
        col_pointer += 1

        self.controltowers = []
        self.ct_labels = []
        self.ct_frame = ScrollableFrame(self.root, width=260, height=800, relief=tk.RAISED, borderwidth=2)
        self.ct_frame.grid(column=col_pointer, row=0, padx=5, pady=5)
        col_pointer += 1

        self.planes = []
        self.plane_labels = []
        self.plane_frame = ScrollableFrame(self.root, width=200, height=800, relief=tk.RAISED, borderwidth=2)
        self.plane_frame.grid(column=col_pointer, row=0, padx=5, pady=5)
        col_pointer += 1

        self.logs_frame = ScrollableFrame(self.root, width=500, height=800, relief=tk.RAISED, borderwidth=2)
        self.logs_frame.grid(column=col_pointer, row=0, padx=5, pady=5)
        self.logs_main_frame = tk.Frame(self.logs_frame.scrollable_frame)
        self.logs_main_frame.pack(padx=5, pady=5)
        col_pointer += 1

        self.root.title("Agentes")
        self.root.geometry("1500x850")


        for agent in agents:
            if agent.__class__.__name__ == "Central":
                self.central.append(agent)
            elif agent.__class__.__name__ == "Airport":
                self.airports.append(agent)
            elif agent.__class__.__name__ == "ControlTower":
                self.controltowers.append(agent)
            elif agent.__class__.__name__ == "Hangar":
                self.hangars.append(agent)
            elif agent.__class__.__name__ == "Plane":
                self.planes.append(agent)

        #* Creating displays for all the agents
        # for a in self.airports:
        #     labels = a.create_display(self.root)
        #     self.agent_labels.append(labels)

        for c in self.central:
            labels = c.create_display(self.central_frame)
            self.central_labels.append(labels)

        for h in self.hangars:
            labels = h.create_display(self.hangar_frame)
            self.hangar_labels.append(labels)

        for ct in self.controltowers:
            labels = ct.create_display(self.ct_frame)
            self.ct_labels.append(labels)

        for p in self.planes:
            labels = p.create_display(self.plane_frame)
            self.plane_labels.append(labels)

        self.update_loop()


    def update_loop(self):
        # for i, a in enumerate(self.airports):
        #     a.update_display(self.agent_labels[i])

        for i, c in enumerate(self.central):
            c.update_display(self.central_labels[i])

        for i, h in enumerate(self.hangars):
            h.update_display(self.hangar_labels[i])

        for i, ct in enumerate(self.controltowers):
            ct.update_display(self.ct_labels[i])
        
        for i, p in enumerate(self.planes):
            p.update_display(self.plane_labels[i])

        for i, log in enumerate(LOGS): #* com ifs, so para ver as divisões entre cada batch de logs
            if i == 0:
                t = f"--\n{log[0]}" 
            elif i == len(LOGS)-1:
                t = f"{log[0]}\n--"
            else:
                t = f"{log[0]}"
            label = tk.Label(self.logs_main_frame, text=t, font='Arial 8', fg=log[1])
            label.pack()
        LOGS.clear()


        self.root.after(1000, self.update_loop)
        
list_agents = []

def changes():
    global list_agents
    while not stop:
        time.sleep(1)
        for a in list_agents:
            a.change_random()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, **kwargs)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")






# AIRPORT_PLANES = {"Lisboa": [3,5], "Porto": [3,5], "Faro": [3,5]} # {localizacao: [num_planes, hangar_capacity]}
# AIRPORT_LOCATIONS = list(AIRPORT_PLANES.keys())
# INTERVAL = 5
# NUM_OF_FLIGHTS_PER_INTERVAL = 2

# class Central():
#     def __init__(self, airport_locations, num_of_flights_per_interval, interval):
#         self.name = "Central"
#         self.airport_locations = airport_locations
#         self.num_of_flights_per_interval = num_of_flights_per_interval
#         self.interval = interval

#     def change_random(self):
#         self.num_of_flights_per_interval = random.randint(1,10)
#         self.interval = random.randint(1,10)


#     def create_display(self, root):
#         label = tk.Label(root, text="Central")
#         label.pack(padx=5, pady=5)

#         frame = tk.Frame(root)
#         frame.pack(padx=10, pady=10)

#         airport_locations = f"Airport Locations: {str(self.airport_locations)}"
#         airport_label = tk.Label(frame, text=airport_locations)
#         airport_label.grid(column=0, row=0, padx=5, pady=5)

#         num_of_flights_per_interval = f"Number of flights per interval: {str(self.num_of_flights_per_interval)}"
#         flights_label = tk.Label(frame, text=num_of_flights_per_interval)
#         flights_label.grid(column=0, row=1, padx=5, pady=5)

#         interval_value = f"Interval: {str(self.interval)}"
#         interval_label = tk.Label(frame, text=interval_value)
#         interval_label.grid(column=0, row=2, padx=5, pady=5)

#         return self.CentralLabels(airport_label, flights_label, interval_label)

#     def update_display(self, labels_obj):
#         labels_obj.airport_label.config(text=f"Airport Locations: {str(self.airport_locations)}")
#         labels_obj.flights_label.config(text=f"Number of flights per interval: {str(self.num_of_flights_per_interval)}")
#         labels_obj.interval_label.config(text=f"Inverval: {str(self.interval)}")

#     class CentralLabels():
#         def __init__(self, airport_label, flights_label, interval_label):
#             self.airport_label = airport_label
#             self.flights_label = flights_label
#             self.interval_label = interval_label

        

    
# class Airport():
#     def __init__(self, location, runways=1):
#         self.name = "Airport0"
#         self.location = location
#         self.runways = runways
#         self.flights_queue = []

#     def change_random(self):
#         self.runways = random.randint(1, 10)
#         self.location = random.choice(["Lisboa", "Porto", "Faro"])

if __name__ == "__main__":
    # c  = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    # c2 = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    # c3 = Central(AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    # a = Airport("Lisboa")
    # list_agents = [c, c2, c3]

    stop = False
    t = threading.Thread(target=changes)
    t.start()

    gui = GUI(list_agents)
    gui.root.mainloop()
    
    stop = True
    print("Acabou!")
