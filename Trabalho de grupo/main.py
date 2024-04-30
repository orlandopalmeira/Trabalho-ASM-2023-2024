import time
import tkinter as tk
import threading
import json

from spade.agent import Agent
from dotenv import load_dotenv
load_dotenv()

# Agents
from Agents.Central.Central import Central
from Agents.Meteo.Meteo import Meteo
from Agents.Airport.Airport import Airport
from Agents.Hangar.Hangar import Hangar
from Agents.Plane.Plane import Plane
from Agents.ControlTower.ControlTower import ControlTower

# Behaviours

# Messages
from Classes.Trip import Trip

# Utils
from Config import Config as cfg
import Utils.GeoDistance as geo
from Utils.Prints import *
from interface import GUI

# DOMAIN = "laptop-140rfmpg.home"
DOMAIN = cfg.DOMAIN #* Para por a correr nos vossos pcs tendes de mudar o DOMAIN no .env
PASSWORD = cfg.PASSWORD


#* Função que lança a interface numa nova thread
stop_thread = False
def gui(agents):
    global stop_thread
    gui = GUI(agents)
    gui.root.mainloop()
    stop_thread = True

def remove_comments(json_str):
    lines = json_str.split("\n")
    lines = [line for line in lines if not line.strip().startswith("//")]
    return "\n".join(lines)

def main():
    #* Configuração
    with open("inputs/input.json", "r") as json_file:
        json_cont = json_file.read()
        json_cont = remove_comments(json_cont)
        config = json.loads(json_cont)
    # AIRPORT_PLANES = {"Lisboa": [3,5,4], "Porto": [3,5,3], "Faro": [3,5,2]} # {localizacao: [num_planes, hangar_capacity, runway_capacity]} #! Tem de se meter aqui a runway_capacity
    AIRPORTS_CONFIG = config["airports"]
    AIRPORT_LOCATIONS = list(AIRPORTS_CONFIG.keys())
    INTERVAL = 10
    NUM_OF_FLIGHTS_PER_INTERVAL = 1

    # WEB interface
    # HOSTNAME = "127.0.0.1"
    # CT_PORT = 1000
    # H_PORT = 2000

    agents = []

    # Airports
    for location in AIRPORT_LOCATIONS:
        airport = Airport(cfg.get_airport_jid(location), PASSWORD, location)
        airport.start().result()
        agents.append(airport)

    # CTs, Hangars and Planes
    current_plane_id = 1
    for location in AIRPORT_LOCATIONS:
        # Interpretação da configuração
        num_planes, hangar_capacity, runways = AIRPORTS_CONFIG[location]
        hangar_availability = hangar_capacity - num_planes
        # Criação do agente CT
        ct = ControlTower(cfg.get_ct_jid(location), PASSWORD, location, runways, hangar_availability)
        ct.start().result()
        agents.append(ct)
        # WEB interface CT
        # ct.web.start(hostname=HOSTNAME, port=CT_PORT)
        # CT_PORT += 1
        
        # Criação do agente Hangar
        hangar = Hangar(cfg.get_hangar_jid(location), PASSWORD, location, hangar_capacity)
        hangar.start().result()
        agents.append(hangar)
        # WEB interface CT
        # hangar.web.start(hostname=HOSTNAME, port=H_PORT)
        # H_PORT += 1

        for _ in range(num_planes):
            plane_name = cfg.get_plane_jid(current_plane_id)
            current_plane_id += 1
            plane = Plane(plane_name, PASSWORD)
            plane.start().result()
            agents.append(plane)
            hangar.add_plane(plane_name)
        
    
    # Central - Só a inicializo aqui para dar tempo aos outros agentes de se inicializarem
    central_jid = cfg.get_central_jid()
    # Flight generation config
    # NUM_OF_FLIGHTS_PER_INTERVAL = flight_config["num_of_flights_per_interval"]
    # INTERVAL = flight_config["interval"]
    flight_config = config["flights"]
    central = Central(central_jid, PASSWORD, AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL, flight_config)
    central.start().result()
    agents.append(central)

    meteo_jid = cfg.get_meteo_jid()
    meteo_mode = Meteo.MODE_MANUAL
    meteo = Meteo(meteo_jid, PASSWORD, AIRPORT_LOCATIONS, meteo_mode)
    meteo.start().result()
    agents.append(meteo)
    

    #* Lancamento da interface
    INTERFACE = True
    if INTERFACE == True:
        t = threading.Thread(target=gui, args=(agents,))
        t.start()

    # while True:
    # while stop_thread == False:
    while any(agent.is_alive() for agent in agents):
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            print_warning("Terminating agents...")
            for agent in agents:
                agent.stop()
            break
    
    if INTERFACE == True:
        t.join()
    
    print_warning(f"\nAgents terminated.\n")


if __name__ == "__main__":
    main()