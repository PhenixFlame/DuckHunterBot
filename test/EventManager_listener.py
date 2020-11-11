from config import TOKEN, BOTFLAG, GUILD_HUNT, CHANNEL_HUNT
from events import EventManager, DecisionTree
from clients import DiscordClient
from decisionTree import TEST_AUTHOR_DECISION_TREE_DICT
from abc_ import Subscriber
from logger import AsyncLogger
import discord

client = DiscordClient()


class EventListener(Subscriber):

    def __init__(self, channel):
        self.logger = AsyncLogger('EventListener')
        self.channel = channel
        self.messages = list()

    async def receive(self, event):
        await self.logger.info(repr(event))


class ChannelListener(Subscriber):

    def __init__(self, channel):
        self.logger = AsyncLogger('ChannelListener')
        self.channel = channel
        self.messages = list()

    async def receive(self, message: discord.Message):
        # if message.channel.name == self.channel.name:
        if message.channel == self.channel:
            self.messages.append(message)
            text = f'{message.author}:{message.content}'
            await self.logger.info(text)


async def initialization():
    await client.ready.wait()
    print('start init')
    HuntChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]

    decision_tree = DecisionTree(TEST_AUTHOR_DECISION_TREE_DICT)
    eventmanager = EventManager(HuntChannel, decision_tree)
    eventlistener = EventListener(HuntChannel)
    channellistener = ChannelListener(HuntChannel)

    eventmanager.subscrive(eventlistener)
    client.subscrive(eventmanager, channellistener)
    print('end init')

client.loop.create_task(initialization())
client.run(TOKEN, bot=BOTFLAG)
