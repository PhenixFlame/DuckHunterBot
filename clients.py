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
    ready = asyncio.Event()
    channels = {}

    async def on_ready(self):
        for c in self.get_all_channels():
            guild = c.guild.name
            self.channels.setdefault(guild, {}).setdefault(c.name, c)

        self.ready.set()
        await self.logger.debug('Logged on as {0}!'.format(self.user))

    async def on_message_edit(self, before, after):
        await self.publish(after)

    async def on_message(self, message):
        await self.publish(message)

    async def get_raw_messages(self, channel, limit=100, before_id=None):
        """
        get raw_messages_data from discord api
        similary iterators.HistoryIterator._retrieve_messages_before_strategy
        """
        data = await self.http.logs_from(channel.id, 100, before=before_id)
        return data


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

