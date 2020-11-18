import asyncio
import re
from collections import deque
from datetime import timedelta

from abc_ import Subscriber, Visitor
from clients import now, Post
from config import HUNTSTARTDELAY, SHOOTWAITTIME, MAX_SIZE_HUNTER_QUEUE
from funcsource import log_errors
from logger import AsyncLogger


class Hunt(Visitor):
    shoottime = timedelta(seconds=HUNTSTARTDELAY)
    waittime = timedelta(seconds=SHOOTWAITTIME)
    closed = False

    def __init__(self):
        super().__init__()
        self.shoottime = now() + timedelta(seconds=HUNTSTARTDELAY)
        self.logger.getChild('init').debug(f'{self} start at [{self.shoottime}]')
        self.closed = False

    async def action(self, hunter, *args, **kwargs):
        if not self.closed and (now() > self.shoottime or len(hunter.hunts) > 2):
            self.logger.getChild('action').debug(f'{hunter} shoot')
            await super(Hunt, self).action(hunter)
        self.shoottime += self.waittime

    async def close(self):
        """
        TODO: close hunter action, if Hunt close
        """
        self.logger.getChild('close').debug(f'{self} closed')
        self.closed = True

    def __repr__(self):
        return type(self).__name__


class Hug(Hunt):
    shoottime = timedelta(seconds=HUNTSTARTDELAY)
    waittime = timedelta(seconds=SHOOTWAITTIME)
    closed = False

    async def action(self, hunter, *args, **kwargs):
        if not self.closed and (now() > self.shoottime or len(hunter.hunts) > 2) and self == hunter.hunts[0]:
            self.logger.getChild('action').debug(f'{hunter} hug')
            await super(Hunt, self).action(hunter)
        self.shoottime += self.waittime


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

    def renew(self, message):
        with log_errors(self.logger):
            match = self.pattern.search(message.content)
            if match:
                self.bullets, self.n_bullets, \
                    self.magazines, self.n_magazines = \
                    map(int, (match[i] for i in [2, 3, 5, 6]))

                self.logger.error(f'new {self}')
            else:
                self.logger.error(f'pattern not found for message: """{message.content}"""')

    def shoot(self):
        if self.bullets:
            self.bullets -= 1
        else:
            self.logger.error(f'shoot without bullets')

    def __repr__(self):
        return 'Ammo(' \
               f'{self.bullets}/{self.n_bullets} bullets, ' \
               f'{self.magazines}/{self.n_magazines} magazines' \
               ')'


class DuckHunter(Subscriber):
    commands = {
        "shoot": "dhpew",
        "reload": "dhreload",
        "buybullet": "dhbuy bullet",
        "buymagazine": "dhbuy magazine",
        "buyweapon": "dhbuy weapon",
        "hug": "dhhug",
    }

    ammo = None

    def __init__(self, post: Post):
        self.events = asyncio.queues.Queue(maxsize=MAX_SIZE_HUNTER_QUEUE)
        self.hunts = deque([Hug()] + [Hunt() for i in range(10)])
        self.post = post
        self.name = post.name
        self.logger = AsyncLogger('Hunter').getChild(post.name)
        self.ammo = Ammo(self)

    def __repr__(self):
        return f'Hunter({self.name}, {self.ammo})'

    async def receive(self, package):
        with log_errors(self.logger):
            if not self.events.full():
                self.events.put_nowait(package)
            else:
                await self.events.put(package)

    async def command(self, text, message=None):
        self.logger.getChild('command').debug(f'command_[{text}]')
        await self.post.send(text)

    async def main_loop(self):
        logger = self.logger.getChild('main_loop')
        logger.debug(f'start main loop')
        with log_errors(logger):
            while True:
                await self.checkammo()

                for hunt in list(self.hunts):
                    await hunt.action(self)

                await self.checkevents()

    async def checkammo(self):
        self.logger.getChild('checkammo').debug(f'{self.ammo}')
        if not self.ammo.bullets:
            if self.ammo.magazines or self.ammo.magazines is None:
                await self.reload()
            elif not self.ammo.magazines:
                if self.ammo.n_bullets > 1:
                    await self.buymagazine()
                    self.ammo.magazines += 1
                else:
                    await self.buybullet()
                    self.ammo.bullets += 1
            else:
                return

            await self.checkevents()

        else:
            return

    async def wait_event(self):
        self.logger.getChild('wait_event').debug(f'await event')
        try:

            if self.hunts:
                events, message = await asyncio.wait_for(self.events.get(), SHOOTWAITTIME)
            else:
                events, message = await self.events.get()

            self.events.task_done()
            for event in events:
                await event.action(self, message=message)
        except asyncio.TimeoutError:
            self.logger.getChild('wait_event').debug(f'timeout waiting event')

    async def checkevents(self):
        # if self.events.empty() and not self.hunts:
        if self.events.empty():
            await self.wait_event()
        else:
            self.logger.getChild('checkevents').debug(f'iterate through events')

        counter = 100  # prevent infinit loop
        while not self.events.empty() and counter > 0:
            counter -= 1
            events, message = self.events.get_nowait()
            for event in events:
                await event.action(self, message=message)

    # EVENT reactions
    async def on_AmmoEvent(self, *args, message, **kwargs):
        self.ammo.renew(message)

    async def on_DuckAppearEvent(self, *args, **kwargs):
        self.hunts.append(Hunt())

    async def on_Hunt(self):
        await self.shoot()

    async def on_Hug(self):
        await self.command('dhhug')
        await self.checkevents()

    async def on_BabyDuckAppear(self, *args, **kwargs):
        self.hunts.append(Hug())

    async def on_DuckDeathEvent(self, *args, **kwargs):
        if self.hunts:
            hunt = self.hunts.popleft()
            await hunt.close()

    async def on_BabyDuckAwait(self, *args, **kwargs):
        if self.hunts:
            hunt = self.hunts.popleft()
            await hunt.close()

    async def on_NoDuckEvent(self, *args, **kwargs):
        while self.hunts:
            hunt = self.hunts.popleft()
            await hunt.close()

    async def shoot(self):
        self.logger.getChild('shoot').debug(f'shoot')
        if self.ammo.bullets:
            await self.command(self.commands['shoot'])
            self.ammo.shoot()

        if not self.ammo.bullets:
            await self.checkammo()
        else:
            await self.checkevents()

    async def reload(self):
        await self.command(self.commands['reload'])

    async def buybullet(self):
        await self.command(self.commands['buybullet'])

    async def buymagazine(self):
        await self.command(self.commands['buymagazine'])

    async def hug(self):
        await self.command(self.commands['hug'])

    async def buyweapon(self):
        await self.command(self.commands['buyweapon'])
