import time
import threading
import json
import sys

from spade import quit_spade
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
from Utils.Prints import *
from interface import GUI

# DOMAIN = "laptop-140rfmpg.home"
DOMAIN = cfg.DOMAIN #* Para por a correr nos vossos pcs tendes de mudar o DOMAIN no .env
PASSWORD = cfg.PASSWORD


#* Função que lança a interface numa nova thread
stop_thread = False
def gui(agents, meteo_mode):
    global stop_thread
    gui = GUI(agents, meteo_mode)
    gui.root.mainloop()
    stop_thread = True

def remove_comments(json_str):
    lines = json_str.split('\n')
    cleaned_lines = []
    for line in lines:
        if '//' in line:
            line = line[:line.index('//')]
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def main():
    #* Configuração
    input_file = "inputs/std.json"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    with open(input_file, "r") as json_file:
        json_cont = json_file.read()
        json_cont = remove_comments(json_cont)
        config = json.loads(json_cont)
    # AIRPORT_PLANES = {"Lisboa": [3,5,4], "Porto": [3,5,3], "Faro": [3,5,2]} # {localizacao: [num_planes, hangar_capacity, runway_capacity]}
    if config.get("airports") == None:
        print_error("No airports configuration found in configuration file.")
        return
    elif config.get("flights") == None:
        print_error("No flights configuration found in configuration file.")
        return
    elif config.get("weather") == None:
        print_error("No weather configuration found in configuration file.")
        return
    AIRPORTS_CONFIG = config["airports"]
    AIRPORT_LOCATIONS = list(AIRPORTS_CONFIG.keys())

    FLIGHT_CONFIG = config["flights"]

    WEATHER_CONFIG = config["weather"]

    # WEB interface
    # HOSTNAME = "127.0.0.1"
    # CT_PORT = 1000
    # H_PORT = 2000

    agents = []

    #* Airports
    for location in AIRPORT_LOCATIONS:
        airport = Airport(cfg.get_airport_jid(location), PASSWORD, location)
        airport.start().result()
        agents.append(airport)

    #* CTs, Hangars and Planes
    current_plane_id = 1
    for location in AIRPORT_LOCATIONS:
        #* Interpretação da configuração
        num_planes, hangar_capacity, runways = AIRPORTS_CONFIG[location]
        hangar_availability = hangar_capacity - num_planes
        #* Criação do agente CT
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
        # WEB interface hangar
        # hangar.web.start(hostname=HOSTNAME, port=H_PORT)
        # H_PORT += 1

        for _ in range(num_planes):
            plane_name = cfg.get_plane_jid(current_plane_id)
            current_plane_id += 1
            plane = Plane(plane_name, PASSWORD)
            plane.start().result()
            agents.append(plane)
            # hangar.add_plane(plane_name)
            hangar.initial_add_plane(plane_name) # Para que não começe a mandar hangar reports à central, sem ela estar sequer criada


    #* Meteo
    meteo_jid = cfg.get_meteo_jid()
    meteo_mode = WEATHER_CONFIG["mode"]
    dt = None
    if meteo_mode == Meteo.MODE_PAST:
        dt = WEATHER_CONFIG["from"]
    meteo = Meteo(meteo_jid, PASSWORD, AIRPORT_LOCATIONS, meteo_mode, datetime=dt)
    meteo.start().result()
    agents.append(meteo) 
    
    #* Central - Só a inicializo aqui para dar tempo aos outros agentes de se inicializarem
    central_jid = cfg.get_central_jid()
    central = Central(central_jid, PASSWORD, AIRPORT_LOCATIONS, FLIGHT_CONFIG)
    central.start().result()
    agents.append(central)
    
    

    #* Lancamento da interface
    INTERFACE = True
    if INTERFACE == True:
        t = threading.Thread(target=gui, args=(agents, meteo_mode))
        t.start()

    # while True:
    # while stop_thread == False:
    # while any(agent.is_alive() for agent in agents):
    while central.is_alive():
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

    # finish all the agents and behaviors running in your process
    quit_spade()


if __name__ == "__main__":
    main()