from typing import AnyStr, Dict, List

import discord

import checkers
from abc_ import Publisher, Subscriber, Visitor
from config import EVENTS
from funcsource import log_errors
from logger import AsyncLogger

LEVELS = {
    'INFO': 20,
    # 'DEBUG': 10,
    'SILENCE': None,
    'NONE': None,
    'None': None,
    'null': None,
    None  : None,
}


class Event(Visitor):
    """
    Composite object for event tree
    Visitor object for Hunter - name is important!
    """
    childs = None
    _checker = checkers.allTrue()
    level = 20  # INFO
    logger = AsyncLogger('Event')

    def __init__(self, name: AnyStr, childs: List or Dict = None):

        if name not in EVENTS:
            raise TypeError(f'Event {name} not found in EVENTS')

        if childs:
            self.childs = list(self.get_childs(childs))

        super().__init__(name)
        self.config()

    async def checker(self, message):
        with log_errors(self.logger):
            return self._checker(message)

    def config(self):
        config = EVENTS.get(self.name)
        if config:
            if 'checker' in config:
                checker, pattern = config['checker']
                self._checker = getattr(checkers, checker)(pattern)

            if 'actions' in config:
                self.actions = config['actions']

            level = config.get('level', 'INFO')
            self.level = LEVELS.get(level, 20)
        # self._pattern = re.compile(pattern)
        # self._checker_ = lambda message: self._pattern.search(message.content)

    def get_childs(self, i):
        """
        build composition of Events
        :param i: next leaf of DECISION_TREE or DECISION_TREE
        :return:
        """
        if isinstance(i, str):
            yield Event(i)
        elif isinstance(i, dict):
            for name, childs_ in i.items():
                yield Event(name, childs_)
        elif isinstance(i, list):
            for c in i:
                yield from self.get_childs(c)

    async def check(self, message):
        if await self.checker(message):
            if self.level:
                yield self

            if self.childs:
                for leaf in self.childs:
                    async for x in leaf.check(message):
                        yield x

    async def events(self, message):
        return [e async for e in self.check(message)]

    def __repr__(self):
        return f"Event({self.name})"


class DecisionTree(Event):

    def __init__(self, tree, name=None):
        name = name or type(self).__name__
        super(DecisionTree, self).__init__(name, childs=tree)

    # TODO
    # def __repr__(self):
    # need tree paint


class EventManager(Publisher, Subscriber):
    decisionTree: DecisionTree

    def __init__(self, channel: discord.TextChannel, decisionTree: DecisionTree):
        self.channel = channel
        self.decisionTree = decisionTree
        self.logger = AsyncLogger(type(self).__name__)

    async def receive(self, message: discord.Message):

        self.logger.debug(f'{self} receive message')

        if self.channel == message.channel:
            events = await self.decisionTree.events(message)
            if events:
                package = events, message
                await self.publish(package)

    def __repr__(self):
        return f"EventManager({self.channel.name}, {self.decisionTree.name})"
