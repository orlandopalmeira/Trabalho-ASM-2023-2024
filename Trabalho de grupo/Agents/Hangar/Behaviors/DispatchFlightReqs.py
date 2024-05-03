from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from Config import Config as cfg
import asyncio
import jsonpickle

class DispatchFlightReqs(OneShotBehaviour):
    lock_atom = asyncio.Lock()

    async def run(self):
        await self.lock_atom.acquire()
        try:
            while True:
                if self.agent.waiting_requests_is_empty():
                    # self.agent.print(f"currently has no waiting requests.", "red")
                    return
                plane_jid = self.agent.pop_plane()
                if plane_jid is None:
                    self.agent.print(f"currently has no planes available.\n\tFlights awaiting availability:\n\t {self.agent.present_waiting_requests()}", "red")
                    return
                trip = self.agent.pop_waiting_requests()
                
                self.agent.print(f"Dispatching {cfg.get_jid_name(plane_jid)} for {trip}")

                ct_jid = cfg.get_ct_jid(self.agent.location)
                plane_and_trip = {
                    'plane_jid': plane_jid,
                    'trip': trip
                }

                msg = Message(to=ct_jid, body=jsonpickle.encode(plane_and_trip), metadata={"performative": "inform"})
                await self.send(msg)

        finally:
            self.lock_atom.release()
