from clients import DiscordClient, Post
from config import TOKEN, BOTFLAG, GUILD_HUNT, CHANNEL_HUNT, DECISION_TREE
from events import EventManager, DecisionTree
from funcsource import log_errors
from hunter import DuckHunter
from logger import AsyncLogger

client = DiscordClient()


async def initialization():
    await client.ready.wait()

    logger = AsyncLogger('initialization')
    with log_errors(logger):
        logger.debug('start initialization')
        HuntChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]

        post = Post(HuntChannel)

        decision_tree = DecisionTree(DECISION_TREE)
        eventmanager = EventManager(HuntChannel, decision_tree)
        duck_hunter = DuckHunter(post)

        eventmanager.subscrive(duck_hunter)
        client.subscrive(eventmanager)

        client.loop.create_task(duck_hunter.main_loop())
        logger.debug('end initialization')

client.loop.create_task(initialization())
client.run(TOKEN, bot=BOTFLAG)
