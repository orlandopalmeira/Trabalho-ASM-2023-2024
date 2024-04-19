import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import random
import jsonpickle
from dotenv import load_dotenv
load_dotenv()

# Agents
from Agents.Central.Central import Central
from Agents.Airport.Airport import Airport
from Agents.Hangar.Hangar import Hangar
from Agents.Plane.Plane import Plane

# Behaviours

# Messages
from Classes.Trip import Trip


# Utils
from Config import Config as cfg
import Utils.GeoDistance as geo

# DOM_NAME = "laptop-140rfmpg.home"
# Talvez meter um .env ou algo do genero para organizar melhor isto nos vários pcs
DOM_NAME = cfg.DOMAIN #* Para por a correr nos vossos pcs tendes de mudar o DOMAIN no .env
PASSWORD = cfg.PASSWORD

def main():
    AIRPORT_PLANES = {"Lisboa": [3,5], "Porto": [3,5], "Faro": [3,5]} # {localizacao: [num_planes, hangar_capacity]}
    AIRPORT_LOCATIONS = list(AIRPORT_PLANES.keys())
    INTERVAL = 5
    NUM_OF_FLIGHTS_PER_INTERVAL = 2

    agents = []

    central_jid = cfg.get_central_jid()
    central = Central(central_jid, PASSWORD, AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    central.start().result()
    agents.append(central)

    for location in AIRPORT_LOCATIONS:
        airport = Airport(cfg.get_airport_jid(location), PASSWORD, location)
        airport.start().result()
        agents.append(airport)

    current_plane_id = 1
    for location in AIRPORT_LOCATIONS:
        hangar = Hangar(cfg.get_hangar_jid(location), PASSWORD, location)
        hangar.start().result()
        agents.append(hangar)
        num_planes, hangar_capacity = AIRPORT_PLANES[location]
        hangar.set_capacity(hangar_capacity)
        for _ in range(num_planes):
            plane_name = cfg.get_plane_jid(current_plane_id)
            current_plane_id += 1
            hangar.add_plane(plane_name)
            plane = Plane(plane_name, PASSWORD)
            plane.start().result()
            agents.append(plane)

    # while True:
    while any(agent.is_alive() for agent in agents):
        try:
            time.sleep(3)
        except KeyboardInterrupt:
            print("Terminating agents...")
            for agent in agents:
                agent.stop()
            break
    
    print(f"\nAgents terminated.\n")


if __name__ == "__main__":
    main()