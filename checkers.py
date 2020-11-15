import discord
import re


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
