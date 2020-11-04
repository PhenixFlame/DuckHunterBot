from config import settings

import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print(message)
        print('Channel:{0.channel}\n'
              '\tMessage from {0.author}:\n'
              '\t\t{0.content}'.format(message))


client = MyClient()
client.run(settings['token'])
