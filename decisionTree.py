import discord
from config import SELF_NAME, DUCK_HUNT_BOT_NAME


def author_checker(author):
    async def cheker(message: discord.Message):
        return str(message.author) == author
    return cheker


TEST_AUTHOR_DECISION_TREE_DICT = {
    author_checker(SELF_NAME): "MyMessageEvent",
    author_checker(DUCK_HUNT_BOT_NAME): "DuckHuntEvent"
}

DECISION_TREE_DICT = {
}

'''
BabyDuckEvent
HuggedBabyEvent

AppearDuckEvent
DuckDeathEvent
ShootEvent
ConfiscateEvent

AmmoEvent
BushsEnvent

'''

