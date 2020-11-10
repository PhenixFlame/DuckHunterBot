from config import settings
from events import EventManager, DecisionTree
from hunter import DuckHunter
from clients import DiscordClient, Post
from decisionTree import DECISION_TREE_DICT

# ____________CONSTANTS________________
TOKEN = settings['token']['bot']
ID_HUNT_CHANNEL = False
# ____________END_CONSTANTS____________

client = DiscordClient()
HuntChannel = client.get_channel(ID_HUNT_CHANNEL)

post = Post(HuntChannel)

decision_tree = DecisionTree(DECISION_TREE_DICT)
eventmanager = EventManager(HuntChannel, decision_tree)
duck_hunter = DuckHunter(post)

eventmanager.subscrive(duck_hunter)
client.subscrive(eventmanager)

client.run(TOKEN)
