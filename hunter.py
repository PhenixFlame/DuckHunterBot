from abc_ import Subscriber, Visitor
from datetime import datetime, timedelta
from clients import now, Post
from logger import AsyncLogger
from collections import deque
import re
from config import HUNTSTARTDELAY, SHOOTWAITTIME, MAX_SIZE_HUNTER_QUEUE
import asyncio
from funcsource import log_errors


class Hunt(Visitor):
    shoottime = HUNTSTARTDELAY
    waittime = SHOOTWAITTIME

    def __init__(self):
        super().__init__()
        self.shoottime = now() + timedelta(seconds=HUNTSTARTDELAY)

    async def action(self, hunter, *args, **kwargs):
        if now() > self.shoottime:
            self.logger.getChild('action').debug(f'{hunter} shoot')
            await super(Hunt, self).action(hunter)
        self.shoottime += self.waittime

    async def close(self):
        """
        TODO: close hunter action, if Hunt close
        """


pattern = (
    r"(Ammunition in the weapon:|Ammo in weapon:)\s*"
    r"(\d)\s*"    r"/\s*"    r"(\d)\s*"
    r"\|\s*"
    r"(Magazines remaining:|Magazines left:)\s*"
    r"(\d)\s*"    r"/\s*"    r"(\d)\s*"
)


class Ammo:
    bullets = None
    magazines = None
    n_bullets = None
    n_magazines = None
    pattern = re.compile(pattern)

    def __init__(self, hunter):
        self.logger = AsyncLogger(hunter.logger).getChild('Ammo')

    def _renew(self, message):
        match = self.pattern.search(message.content)
        if match:
            _, self.bullets, self.n_bullets,\
            _, self.magazines, self.n_magazines = \
                match.groups()
        else:
            self.logger.error(f'pattern not found for message: """{message.content}"""')

    def shoot(self):
        if self.bullets:
            self.bullets -= 1
        else:
            self.logger.error(f'shoot without bullets')

    async def renew(self, message):
        self._renew(message)

    def __repr__(self):
        return 'Ammo(' \
               f'bullets={self.bullets}/{self.n_bullets}, ' \
               f'magazines={self.magazines}/{self.n_magazines}' \
               ')'


class DuckHunter(Subscriber):
    commands = {
        "shoot": "dhpew",
        "reload": "dhreload",
        "buybullet": "dhbuy bullet",
        "buymagazine": "dhbuy magazine",
        "hug": "dhhug",
    }

    ammo = None

    def __init__(self, post: Post):
        self.events = asyncio.queues.Queue(maxsize=MAX_SIZE_HUNTER_QUEUE)
        self.hunts = deque()
        self.post = post
        self.name = post.name
        self.logger = AsyncLogger('Hunter').getChild(post.name)
        self.ammo = Ammo(self)

        for attr, text in self.commands.items():
            async def f(): await self.command(text)

            f.__name__ = attr
            setattr(self, attr, f)

    def __repr__(self):
        return f'Hunter({self.name}, {self.ammo})'

    async def receive(self, events):
        with log_errors(self.logger):
            for e in events:
                if not self.events.full():
                    self.events.put_nowait(e)
                else:
                    await self.events.put(e)

    async def command(self, text):
        self.logger.getChild('command').debug(f'command_[{text}]')
        await self.post.send(text)

    async def main_loop(self):
        logger = self.logger.getChild('main_loop')
        logger.debug(f'start main loop')
        with log_errors(logger):
            while True:
                await self.checkammo()
                await self.checkevents()

                for hunt in self.hunts:
                    await hunt.action(self)

    async def _shoot(self):
        self.logger.getChild('shoot').debug(f'shoot')
        if not self.ammo.bullets:
            await self.checkammo()
        self.ammo.shoot()
        await self.shoot()
        await self.checkevents()

    async def checkammo(self):
        self.logger.getChild('checkammo').debug(f'{self.ammo}')
        if not self.ammo.bullets:
            if self.ammo.magazines or self.ammo.magazines is None:
                await self.reload()
                await self.checkevents()
            elif not self.ammo.magazines:
                if self.ammo.n_bullets > 1:
                    await self.buymagazine()
                    self.ammo.magazines += 1
                    await self.checkevents()
                else:
                    self.buybullet()
                    self.ammo.bullets += 1
                    await self.checkevents()

    async def checkevents(self):
        if self.events.empty():
            self.logger.getChild('checkevents').debug(f'await events')
            events, message = await self.events.get()
            for event in events:
                await event.action(self, message=message)
            self.events.task_done()
        else:
            self.logger.getChild('checkevents').debug(f'while events')

        counter = 100  # prevent infinit loop
        while not self.events.empty() and counter > 0:
            counter -= 1
            events, message = self.events.get_nowait()
            for event in events:
                await event.action(self, message=message)

    # EVENT reactions
    async def on_AmmoEvent(self, *args, message, **kwargs):
        self.ammo._renew(message)
        
    async def on_DuckAppearEvent(self, *args, **kwargs):
        self.hunts.append(Hunt())

    async def on_Hunt(self):
        await self._shoot()

    async def on_DuckDeathEvent(self, *args, **kwargs):
        hunt = self.hunts.popleft()
        await hunt.close()

    async def on_JammedWeaponEvent(self, *args, **kwargs):
        await self.reload()
    
    async def on_NoDuckEvent(self, *args, **kwargs):
        del self.events
        self.events = asyncio.queues.Queue(maxsize=MAX_SIZE_HUNTER_QUEUE)

    async def on_WeaponConfiscatedEvent(self, *args, **kwargs):
        await self.reload()

