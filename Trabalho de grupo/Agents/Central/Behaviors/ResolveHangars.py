import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Config import Config as cfg

import Utils.GeoDistance as geo

from Classes.Trip import Trip
from Classes.HangarReport import HangarReport

class ResolveHangars(PeriodicBehaviour):

    async def run(self):
        crowded_hangars = self.agent.crowded_hangars
        scarse_hangars = self.agent.scarse_hangars

        trips = []
        crowded_index = 0
        scarse_index  = 0

        # TODO Verificar melhor funcionamento disto e talvez meter algo que caso haja hangares ha mt tempo sem serem tratados, fazer com que seja gerado uma viagem para eles com o aeroporto mais proximo com a função get_nearest_city()

        #* Initial simple implementation
        while crowded_index < len(crowded_hangars) and scarse_index < len(scarse_hangars):
            crowded_site = crowded_hangars[crowded_index].get_location()
            scarse_site = scarse_hangars[scarse_index].get_location()
            trip = Trip(crowded_site, scarse_site, type_flight="balance")
            trips.append(trip)
            crowded_index += 1
            scarse_index += 1
           
        for trip in trips:
            msg = self.agent.create_trip_msg(trip)
            await self.send(msg)