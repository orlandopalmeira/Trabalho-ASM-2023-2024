import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import random
import jsonpickle

# Agents
from Agents.Central import Central
from Agents.Airport import Airport
from Agents.Hangar import Hangar
from Agents.Plane import Plane

# Behaviours

# Messages
from Classes.Trip import Trip


# Utils
from Utils.TripGenerator import generate_random_trips, generate_random_trip
import Utils.GeoDistance as geo

# Talvez meter um .env ou algo do genero para organizar melhor isto nos vários pcs
DOM_NAME = "laptop-140rfmpg.home"


def main():
    AIRPORT_LOCATIONS = ["Lisboa", "Porto", "Faro"]
    NUM_PLANES = 5
    INTERVAL = 5
    NUM_OF_FLIGHTS_PER_INTERVAL = 2

    agents = []

    central = Central(f"central@{DOM_NAME}", "NOPASSWORD")
    central.start().result()
    agents.append(central)

    for location in AIRPORT_LOCATIONS:
        airport = Airport(f"airport_{location}@{DOM_NAME}", "NOPASSWORD")
        airport.start().result()
        agents.append(airport)
        hangar = Hangar(f"hangar_{location}@{DOM_NAME}", "NOPASSWORD")
        hangar.start().result()
        agents.append(hangar)

    for i in range(NUM_PLANES):
        plane = Plane(f"plane{i}@{DOM_NAME}", "NOPASSWORD")
        plane.start().result()
        agents.append(plane)

    # while True:
    while any(agent.is_alive() for agent in agents):
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("Terminating agents...")
            for agent in agents:
                agent.stop()
            break
    
    print(f"\n\nAgents terminated.")


if __name__ == "__main__":
    main()