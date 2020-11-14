import discord
from config import SELF_NAME, DUCK_HUNT_BOT_NAME
from abc_ import Visitor
import re


EVENTS = {
    # _______________DuckEvents_______________________
    "DuckAppearEvent": '<:official_Duck_01_reversed:439576463436546050>',

    "DuckDeathEvent": r"You killed the duck in"  # DuckKilledEvet
                      
                      r"|The duck (went"  # DuckFlewAway
                          r"|flew"
                          r"|left"
                          r"|dissipated"
                          r"|chickened"
                          r"|didn't have time"
                          r"|doesn't want"
                          r"|walked up"
                          r")"
                      
                      r"|**FLAPP**"  # DuckFrightenedEvent
                      r")",

    # TODO: DuckBabyEvents"
    "NoDuckEvent": "There isn't any duck",

    # ___________IAmMentionedEvents___________________
    "AmmoEvent": r"Ammo in weapon"
                 r"|MAGAZINE EMPTY",

    "WeaponConfiscatedEvent": r"You don't have a weapon"
                              r"|weapon confiscated",

    "JammedWeaponEvent": "Your weapon (is|just) jammed",

    # TODO ShootEvent
    # TODO IAmWetEvent
    # TODO BushsEnvent
}


def author_checker(author):
    """
    :param author: format: 'an_fenix#2270'
    :return:
    """

    async def cheker(message: discord.Message):
        return str(message.author) == author

    return cheker


def mention_checker(name):
    """
    :param name: format: 'an_fenix#2270'
    :return:
    """

    async def cheker(message: discord.Message):
        return str(message.mentions[0]) == name

    return cheker


TEST_AUTHOR_DECISION_TREE_DICT = {
    author_checker(SELF_NAME): "MyMessageEvent",
    author_checker(DUCK_HUNT_BOT_NAME): "DuckHuntEvent"
}

DECISION_TREE_DICT = {
}


class Event(Visitor):
    def __init__(self, name):
        super().__init__(name)
        p = re.compile(EVENTS[self.name])
        self._checker_ = lambda message: p.search(message.content)

    def check(self, message: discord.Message):
        return self._checker_(message)
