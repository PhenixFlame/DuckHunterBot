from config import settings
from logger import AsyncLogger
from hunter import DuckHunter
from clients import DiscordClient, Post
from decisionTree import DECISION_TREE_DICT
from abc_ import Subscriber

# ____________CONSTANTS________________
TOKEN = settings['token']['bot']
GUILD_HUNT = 'Сервер an_fenix'
CHANNEL_HUNT = 'test'
ID_HUNT_CHANNEL = False
# ____________END_CONSTANTS____________

client = DiscordClient()


class Listener(Subscriber):

    def __init__(self, channel):
        self.logger = AsyncLogger('Listener')
        self.channel = channel
        self.messages = list()

    async def receive(self, message):
        # if message.channel.name == self.channel.name:
        if message.channel == self.channel:
            self.messages.append(message)
            await self.logger.info(message.content)


async def initialization():
    await client.ready.wait()

    HuntChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]

    listener = Listener(HuntChannel)
    client.subscrive(listener)


client.loop.create_task(initialization())
client.run(TOKEN)
