from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import jsonpickle
from Classes.Trip import Trip
from Config import Config as cfg
from Utils.Prints import *

class GenerateFlightsBehav(PeriodicBehaviour):
    async def run(self):
        print()
        for _ in range(self.agent.num_of_flights_per_interval):
            trip = None
            if self.agent.flight_plan is not None:
                idx = self.agent.flight_plan_index
                if not self.agent.repeat_flight_plan and idx >= len(self.agent.flight_plan):
                    self.kill()
                    return
                origin, dest = self.agent.flight_plan[idx]
                trip = Trip(origin, dest)
                self.agent.flight_plan_index = (idx + 1)
                if self.agent.repeat_flight_plan:
                    self.agent.flight_plan_index %= len(self.agent.flight_plan)
            # RANDOM TRIP GENERATION
            else:
                trip = Trip.generate_random_trip(self.agent.airport_locations)

            print_info(f"CENTRAL: Flight generated {trip}")
            airport_name = cfg.get_airport_jid(trip.get_origin())
            msg = Message(to=airport_name, metadata={'performative':'request'}, body=jsonpickle.encode(trip))
            await self.send(msg) #> Use case 1: passo 1
            self.agent.add_to_historic(trip)
        print()

        # # Pretty Printing das viagens geradas
        # print()
        # for trip in trips:
        # print()
        # ###
        
        # for trip in trips:

