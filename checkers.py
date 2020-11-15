import discord
import re
import config


def author_checker(author):
    """
    :param author: format: 'an_fenix#2270'
    :return:
    """

    # author may be constant as SELF_NAME or DUCK_HUNT_BOT_NAME from config
    if hasattr(config, author):
        author = getattr(config, author)

    async def cheker(message: discord.Message):
        return str(message.author) == author

    return cheker


def mention_checker(name):
    """
    :param name: format: 'an_fenix#2270'
    :return:
    """

    # author may be constant as SELF_NAME or DUCK_HUNT_BOT_NAME from config
    if hasattr(config, name):
        name = getattr(config, name)

    async def cheker(message: discord.Message):
        return str(message.mentions[0]) == name

    return cheker


def allTrue():
    return _allTrue


def _allTrue(message):
    return True


def regex(pattern_):
    pattern = re.compile(pattern_)

    def search(message):
        return bool(pattern.search(message.content))

    search.pattern = pattern_

    return search
