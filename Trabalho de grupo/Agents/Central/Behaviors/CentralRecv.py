import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Config import Config as cfg

# from Classes.Trip import Trip
from Classes.HangarReport import HangarReport

class RecvRequests(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=20)
        if not msg:
            # self.agent.print("No message received")
            return
        
        if msg.metadata["performative"] == "inform" and cfg.identify(msg.sender) == "hangar":
            report: HangarReport = jsonpickle.decode(msg.body)
            type_of_req = report.get_type()
            if type_of_req == HangarReport.CROWDED:
                self.agent.add_to_crowded_hangars(report)
            elif type_of_req == HangarReport.SCARSE:
                self.agent.add_to_scarse_hangars(report)

        else:
            self.agent.print(f"WARNING - Received unknown message from {cfg.get_jid_name(msg.sender)}", "red")
