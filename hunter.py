from abc_ import Subscriber, Visitor
from datetime import datetime, timedelta

# ____________CONSTANTS________________

HUNTSTARTDELAY = 500  # seconds
SHOOTWAITTIME = 5  # seconds
now = datetime.now

# ____________END_CONSTANTS____________


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


class DuckHunter(Subscriber):
    commands = {
        "shoot": "dhpew",
        "reload": "dhreload",
        "buybullet": "dhbuy bullet",
        "buymagazine": "dhbuy magazine",
        "hug": "dhhug",
    }

    ammo = None

    def __init__(self, post):
        self.events = list()
        self.hunts = list()
        self.post = post

        for attr, text in self.commands.items():
            async def f(): await self.command(text)

            f.__name__ = attr
            setattr(self, attr, f)
    
    async def receive(self, events):
        self.events.extend(events)
    
    async def command(self, text):
        await self.post.send(text)

    async def main_loop(self):
        for event in self.events:
            await event.action(self)

        for hunt in self.hunts:
            await hunt.action(self)

        await self.checkammo()

    async def on_Hunt(self):
        await self.shoot()

    async def on_DuckBirthEvent(self):
        self.hunts.append(Hunt())

    async def checkevents(self):
        pass

    async def checkammo(self):
        pass
