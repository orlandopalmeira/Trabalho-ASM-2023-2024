# Basic template for a behaviour file

from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour, Behaviour
from spade.message import Message

class ReceiveRequestBehav(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg and msg.get_metadata('performative') == 'request':
            msg_splitted = msg.body.split(';')
            product = msg_splitted[0]
            quantity = int(msg_splitted[1])
            print(f'Agent {self.agent.jid}: Message from buyer: {msg.body}')
            if product in self.agent.products and quantity > 0:
                self.agent.products_sold[product] += quantity
                await self.send(Message(to=str(msg.sender), metadata={'performative':"confirm"}, body=f'Product \'{product}\' available'))
            else:
                await self.send(Message(to=str(msg.sender), metadata={'performative':'refuse'}, body=f'Product \'{product}\' unavailable'))