import abc
from logger import getLogger


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

    async def _publish(self, message):
        for s in self.subscribers:
            await s.receive(message)

    def subscrive(self, s):
        self.subscribers.add(s)

    def unsubscrive(self, s):
        self.subscribers.discard(s)


class Visitor(abc.ABC):

    def __init__(self):
        self.name = type(self).__name__
        self.logger = getLogger(self.name)

    @abc.abstractmethod
    async def action(self, obj):
        method = 'on_' + self.name
        try:
            getattr(obj, method)()
        except AttributeError:
            self.logger.info(f'{type(obj)} doesn`t have action on {self.name}')
