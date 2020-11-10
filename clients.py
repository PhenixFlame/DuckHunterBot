import discord
from abc_ import Publisher
from logger import AsyncLogger
from datetime import datetime, timedelta
import asyncio

# ____________CONSTANTS________________

POST_MESSAGE_PERIOD = 0.5  # seconds
now = datetime.now

# ____________END_CONSTANTS____________


class DiscordClient(discord.Client, Publisher):
    logger = AsyncLogger('DiscordClient')

    async def on_ready(self):
        await self.logger.debug('Logged on as {0}!'.format(self.user))

    async def on_message_edit(self, before, after):
        await self.publish(after)

    async def on_message(self, message):
        await self.publish(message)


class Post:
    """
    Interface for control sending messages processes
    """
    messageInterval: timedelta
    nextTimeSend = None

    def __init__(self, channel: discord.TextChannel, delay=POST_MESSAGE_PERIOD):
        """
        :param channel: discord.TextChannel will used for send messages
        :param delay: in seconds
        """
        self.messageInterval = timedelta(seconds=delay)
        self.channel = channel
        self.nextTimeSend = now()

    async def send(self, text):
        """
        Send text to channel, controlling time interval between messages
        :param text:
        :return:
        """

        # check message last time
        wait_time = (self.nextTimeSend - now()).total_seconds()
        if wait_time > 0:
            await asyncio.sleep(wait_time)

        message = await self.channel.send(text)
        self.nextTimeSend = message.created_at + self.messageInterval

