import discord

from abc_ import Visitor

yamls = """
NoDuckEvent: '"There isn''t any duck" in message.content'
"""

pythond = {
    "NoDuckEvent": '"There isn\'t any duck" in message.content'
}

# d = yaml.safe_load(io.StringIO(yamls))
d = pythond


class Event(Visitor):
    def __init__(self, name):
        super().__init__(name)
        self._checker_ = d[self.name]

    def check(self, message: discord.Message):
        return eval(self._checker_)


testevent = Event('NoDuckEvent')


class TestMessage:
    content = "There isn't any"


testmessage = TestMessage()

if __name__ == '__main__':
    xx = testevent.check(testmessage)
    print(xx)

# for History
EVAL_EVENTS = {
    "NoDuckEvent": '"There isn\'t any duck" in message.content',
    "DuckAppearEvent": "'<:official_Duck_01_reversed:439576463436546050>' in message.content",
    "DuckDeathEvent": """
        re.search(
            r"The duck (went|flew|left|dissipated|chickened|didn't have time|doesn't want|walked up)",
            message.content
        )"""
}

RE_EVENTS = {
    "NoDuckEvent": "There isn't any duck",
    "DuckAppearEvent": '<:official_Duck_01_reversed:439576463436546050>',
    "DuckDeathEvent": r"The duck (went"
                      r"|flew"
                      r"|left"
                      r"|dissipated"
                      r"|chickened"
                      r"|didn't have time"
                      r"|doesn't want"
                      r"|walked up"
                      r")",

}
