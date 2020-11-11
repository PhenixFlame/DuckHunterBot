from config import TOKEN, BOTFLAG, GUILD_HUNT, CHANNEL_HUNT
from clients import DiscordClient
import discord
import funcsource as fs

client = DiscordClient()
Messages = []
Timer = fs.Timer()


async def initialization():
    await client.ready.wait()

    HuntChannel: discord.TextChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]

    print('Start read history')
    Messages = await client.get_raw_messages(HuntChannel, 1000)
    print(
        'Write file: ',
        fs.write_file('resources/messages_1000.pkl', Messages, 'pkl')
    )
    await client.close()

client.loop.create_task(initialization())
client.run(TOKEN, bot=BOTFLAG)
