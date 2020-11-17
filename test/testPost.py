from clients import DiscordClient, Post
from config import TOKEN, BOTFLAG, GUILD_HUNT, CHANNEL_HUNT
from logger import AsyncLogger

client = DiscordClient()


async def initialization():
    await client.ready.wait()

    HuntChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]
    logger = AsyncLogger('initialization')
    post = Post(HuntChannel, delay=5)
    for i in ['hello'] + [str(i) for i in range(10)]:
        logger.debug(f'send "{i}"')
        await post.send(i)

    await client.close()

client.loop.create_task(initialization())
client.run(TOKEN, bot=BOTFLAG)
