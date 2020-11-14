from abc_ import Publisher, Subscriber, Visitor
from logger import AsyncLogger
import discord
from decisionTree import Event


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
        except AttributeError as e:

            if tree is None:
                self.logger.info(f'No Event for message: \n\t{message.content}')

            if not isinstance(tree, Event):
                self.logger.critical(f'tree is not Event! message: \n\t{message.content}')

            self.logger.debug(f'{repr(tree)} for "{message.content}"')
            return tree
        except Exception as e:
            self.logger.error(f'ERROR {e} for message: \n\t{message.content}')
            raise e


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


class NoDecisionError(Exception):
    def __init__(self, message):
        self.message = message











