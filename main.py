from config import settings
from events import EventManager, DecisionTree
from hunter import DuckHunter
from clients import DiscordClient, Post
from decisionTree import DECISION_TREE_DICT

# ____________CONSTANTS________________
TOKEN = settings['token']['bot']
GUILD_HUNT = 'Сервер an_fenix'
CHANNEL_HUNT = 'test'
ID_HUNT_CHANNEL = False
# ____________END_CONSTANTS____________

client = DiscordClient()


async def initialization():
    await client.ready.wait()

    HuntChannel = client.channels[GUILD_HUNT][CHANNEL_HUNT]

    post = Post(HuntChannel)

    decision_tree = DecisionTree(DECISION_TREE_DICT)
    eventmanager = EventManager(HuntChannel, decision_tree)
    duck_hunter = DuckHunter(post)

    eventmanager.subscrive(duck_hunter)
    client.subscrive(eventmanager)

client.run(TOKEN)
