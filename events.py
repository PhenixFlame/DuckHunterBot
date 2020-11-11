from abc_ import Publisher, Subscriber, Visitor
from logger import AsyncLogger
import discord


def build_event_tree(tree):
    if isinstance(tree, str):
        return Event(tree)
    return {
        i: build_event_tree(tree_)
        for i, tree_ in tree.items()
    }


class DecisionTree:
    def __init__(self, tree_dict):
        self.logger = AsyncLogger(type(self).__name__)
        self.tree_dict = build_event_tree(tree_dict)

    async def decision(self, message):
        return await self._decision(message, self.tree_dict)

    async def _decision(self, message: discord.Message, tree):
        try:
            for check, next_tree in tree.items():
                if await check(message):
                    return await self._decision(message, next_tree)
        except Exception as e:
            if tree is None:
                await self.logger.info(f'{e} for message: \n\t{message.content}')

            return tree


class EventManager(Publisher, Subscriber):
    decisionTree = tuple()

    def __init__(self, channel: discord.TextChannel, decisionTree: DecisionTree):
        self.channel = channel
        self.decisionTree = decisionTree

    async def receive(self, message: discord.Message):
        if self.channel == message.channel:
            event = await self.decisionTree.decision(message)
            if event:
                await self.publish(event)


class Event(Visitor):
    def __init__(self, name):
        self.name = name
        self.logger = AsyncLogger(type(self).__name__)


class NoDecisionError(Exception):
    def __init__(self, message):
        self.message = message











