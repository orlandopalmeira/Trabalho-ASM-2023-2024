from spade.behaviour import OneShotBehaviour
from spade.message import Message

# from Agents.Hangar.Hangar import Hangar

from Config import Config as cfg
from Classes.HangarReport import HangarReport

import jsonpickle


class SendHangarRep(OneShotBehaviour):

    async def run(self):
        if self.agent.is_too_full():
            prio = self.agent.get_priority()
            hangar_rep = HangarReport(HangarReport.CROWDED, self.agent.location, prio)
            central_jid = cfg.get_central_jid()
            msg = Message(to=central_jid, 
                          body=jsonpickle.encode(hangar_rep), 
                          metadata={"performative": "inform"})
            await self.send(msg)

        elif self.agent.is_too_empty():
            prio = self.agent.get_priority()
            hangar_rep = HangarReport(HangarReport.SCARSE, self.agent.location, prio)
            central_jid = cfg.get_central_jid()
            msg = Message(to=central_jid,
                          body=jsonpickle.encode(hangar_rep),
                          metadata={"performative": "inform"})
            await self.send(msg)