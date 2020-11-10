import abc
from logger import getLogger


class NoActionError(Exception):
    def __init__(self, message, e):
        self.message = message
        self.error = e


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
            await s.receive(message)

    def subscrive(self, s):
        self.subscribers.add(s)

    def unsubscrive(self, s):
        self.subscribers.discard(s)


class Visitor(abc.ABC):
    """
    raise NoActionError if there doesn't exist action for Visitor
    """

    def __init__(self):
        self.name = type(self).__name__
        self.logger = getLogger(self.name)

    async def action(self, obj):
        method = 'on_' + self.name
        try:
            getattr(obj, method)()
        except AttributeError as e:
            raise NoActionError(f'{type(obj)} doesn`t have action on {self.name}', e)
