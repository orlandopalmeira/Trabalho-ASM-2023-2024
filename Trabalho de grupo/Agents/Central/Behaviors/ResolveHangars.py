import jsonpickle, time
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Config import Config as cfg

import Utils.GeoDistance as geo

from Classes.Trip import Trip
from Classes.HangarReport import HangarReport

class ResolveHangars(PeriodicBehaviour):

    async def run(self):
        #! Talvez deva meter locks nisto para mexer nestas listas de hangar_reps 
        crowded_hangars = self.agent.crowded_hangars.copy()
        scarse_hangars = self.agent.scarse_hangars.copy()

        trips = []
        crowded_index = 0
        scarse_index  = 0

        #* Initial simple implementation
        while crowded_index < len(crowded_hangars) and scarse_index < len(scarse_hangars):
            crowded_rep: HangarReport = crowded_hangars[crowded_index]
            scarse_rep:  HangarReport = scarse_hangars[scarse_index]
            crowded_loc = crowded_rep.get_location()
            scarse_loc  = scarse_rep.get_location()
            trip = Trip(crowded_loc, scarse_loc, type_flight="balance")
            trips.append(trip)
            crowded_index += 1
            scarse_index += 1

        # Remover hangars que já foram resolvidos
        for trip in trips:
            self.agent.crowded_hangars = [hr for hr in crowded_hangars if hr.get_location() != trip.get_origin()]
            self.agent.scarse_hangars  = [hr for hr in scarse_hangars if hr.get_location() != trip.get_destination()]

        #??? Func extra (talvez comentar para não confundir)
        # old_crowded_locations = map(lambda obj: obj.get_location(), crowded_hangars)
        # old_scarse_locations  = map(lambda obj: obj.get_location(), scarse_hangars)
        # crowded_hangars = self.agent.crowded_hangars.copy()
        # scarse_hangars = self.agent.scarse_hangars.copy()
        # MAX_WAIT = 20
        # # Checkar por reports antigos que ainda não foram resolvidos
        # if len(crowded_hangars) == 0 and len(scarse_hangars) > 0:
        #     possible_locations = [item for item in scarse_hangars if item.get_location() not in old_scarse_locations]
        #     for hr in scarse_hangars:
        #         if hr.get_priority() > 0 or time.time() - hr.get_timestamp < MAX_WAIT: # So faz isto para hangares que estão completamente cheios/vazios e que estão à espera há mais de MAX_WAIT segundos
        #             continue
        #         closest_location = geo.get_nearest_city(hr.get_location(), possible_locations)
        #         trips.append(Trip(closest_location, hr.get_location(), type_flight="balance"))
        # elif len(scarse_hangars) == 0 and len(crowded_hangars) > 0:
        #     possible_locations = [item for item in crowded_hangars if item.get_location() not in old_crowded_locations]
        #     for hr in crowded_hangars:
        #         if hr.get_priority() > 0 or time.time() - hr.get_timestamp < MAX_WAIT: # So faz isto para hangares que estão completamente cheios/vazios e que estão à espera há mais de MAX_WAIT segundos
        #             continue
        #         closest_location = geo.get_nearest_city(hr.get_location(), possible_locations)
        #         trips.append(Trip(hr.get_location(), closest_location, type_flight="balance"))
        
        # # Remoção de hangars resolvidos
        # for trip in trips:
        #     self.agent.crowded_hangars = [hr for hr in crowded_hangars if hr.get_location() != trip.get_origin()]
        #     self.agent.scarse_hangars  = [hr for hr in scarse_hangars if hr.get_location() != trip.get_destination()]
        #??? Fim func extra
        
        # Enviar trips
        for trip in trips:
            msg = self.agent.create_trip_msg(trip)
            await self.send(msg)