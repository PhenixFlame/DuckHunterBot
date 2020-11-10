from logger import AsyncLogger
import discord


class NoDecisionError(Exception):
    def __init__(self, message):
        self.message = message


class DecisionTree:
    def __init__(self, tree_dict):
        self.logger = AsyncLogger(type(self).__name__)
        self.tree_dict = tree_dict

    async def decision(self, message):
        return await self._decision(message, self.tree_dict)

    async def _decision(self, message: discord.Message, tree):
        try:
            for check, next_tree in tree.items():
                if await check(message):
                    return await self._decision(message, next_tree)
        except Exception as e:
            if tree is None:
                await self.logger.info(f'{e} for message: \n\t{message.content}')

            return tree


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

