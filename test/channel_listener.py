from logger import AsyncLogger
from clients import DiscordClient, Post
from abc_ import Subscriber
import discord
from config import TOKEN, GUILD_HUNT, CHANNEL_HUNT

client = DiscordClient()


class Listener(Subscriber):

    def __init__(self, channel):
        self.logger = AsyncLogger('Listener')
        self.channel = channel
        self.messages = list()

    async def receive(self, message: discord.Message):
        # if message.channel.name == self.channel.name:
        if message.channel == self.channel:
            self.messages.append(message)
            text = f'{message.author} : {message.content}'
            self.logger.info(text)


async def initialization():
    await client.ready.wait()

    HuntChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]

    listener = Listener(HuntChannel)
    client.subscrive(listener)


client.loop.create_task(initialization())
client.run(TOKEN)
