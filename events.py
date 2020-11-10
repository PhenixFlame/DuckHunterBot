from abc_ import Publisher, Subscriber, Visitor
from decisionTree import DecisionTree
from discord import TextChannel, Message
from datetime import datetime, timedelta
from logger import AsyncLogger

# ____________CONSTANTS________________

HUNTSTARTDELAY = 500  # seconds
SHOOTWAITTIME = 5  # seconds
now = datetime.now

# ____________END_CONSTANTS____________


class EventManager(Publisher, Subscriber):
    decisionTree = tuple()

    def __init__(self, channel: TextChannel, decisionTree: DecisionTree):
        self.channel = channel
        self.decisionTree = decisionTree

    async def receive(self, message: Message):
        if self.channel == message.channel:
            event = await self.decisionTree.decision(message)
            if event:
                await self.publish(event)


class Event(Visitor):
    def __init__(self, name):
        self.name = name
        self.logger = AsyncLogger(type(self).__name__)


class Hunt(Visitor):
    shoottime = HUNTSTARTDELAY
    waittime = SHOOTWAITTIME

    def __init__(self):
        super().__init__()
        self.shoottime = now() + timedelta(seconds=HUNTSTARTDELAY)

    async def action(self, hunter):
        if now() > self.shoottime:
            await super(Hunt, self).action(hunter)
        self.shoottime += self.waittime

    def close(self):
        """
        TODO: close hunter action, if Hunt close
        """








