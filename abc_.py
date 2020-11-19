import abc
import asyncio

from logger import AsyncLogger


class Subscriber(abc.ABC):
    @abc.abstractmethod
    async def receive(self, message):
        pass


class Publisher:
    """
    ABC Interface of Publisher
    """
    _subscribers: set = tuple()

    @property
    def subscribers(self):
        if not self._subscribers:
            self._subscribers = set()
        return self._subscribers

    async def publish(self, message):
        for s in self.subscribers:
            #        receive can be block!
            asyncio.create_task(s.receive(message))

    def subscrive(self, *s):
        self.subscribers.update(s)

    def unsubscrive(self, *s):
        self.subscribers.difference_update(s)


class Visitor(abc.ABC):
    """
    raise NoActionError if there doesn't exist action for Visitor
    """
    logger = AsyncLogger('Visitor')

    def __init__(self, name=None):
        self.name = name or type(self).__name__
        self.logger = self.logger.getChild(self.name)
        self.actions = dict()

    async def action(self, obj, *args, **kwargs):
        method = 'on_' + self.name
        try:
            await getattr(obj, method)(*args, **kwargs)
            self.logger.debug(f'{type(obj)} action on {self.name}')
        except AttributeError:
            try:
                method, *args = self.actions[type(obj).__name__]
                await getattr(obj, method)(*args, **kwargs)
                self.logger.debug(f'{type(obj)} action on {self.name}')
            except (KeyError, AttributeError):
                self.logger.debug(f'{type(obj)} doesn`t have action on {self.name}')

    def __repr__(self):
        return f"{type(self).__name__}({self.name})"
