import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import random
import jsonpickle

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

# Talvez meter um .env ou algo do genero para organizar melhor isto nos vários pcs
# DOM_NAME = "laptop-140rfmpg.home"
DOM_NAME = cfg.get_domain_name()


def main():
    AIRPORT_LOCATIONS = ["Lisboa", "Porto", "Faro"]
    NUM_PLANES = 5
    INTERVAL = 5
    NUM_OF_FLIGHTS_PER_INTERVAL = 2

    agents = []

    central_jid = cfg.get_central_jid()
    central = Central(central_jid, "NOPASSWORD", AIRPORT_LOCATIONS, NUM_OF_FLIGHTS_PER_INTERVAL, INTERVAL)
    central.start().result()
    agents.append(central)

    for location in AIRPORT_LOCATIONS:
        airport = Airport(cfg.get_airport_jid(location), "NOPASSWORD", location)
        airport.start().result()
        agents.append(airport)
        hangar = Hangar(cfg.get_hangar_jid(location), "NOPASSWORD", location)
        hangar.start().result()
        agents.append(hangar)

    #! Maneira de criar aviões terá de ser feita consoante os hangares para adicionar os jids aos hangares
    for i in range(NUM_PLANES):
        plane = Plane(cfg.get_plane_jid(i), "NOPASSWORD")
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