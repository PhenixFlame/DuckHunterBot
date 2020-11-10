from abc_ import Publisher, Subscriber, Visitor
from decisionTree import DecisionTree
from discord import TextChannel, Message
from logger import AsyncLogger


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









