from clients import DiscordClient
from config import TOKEN

# TOKEN = settings['token']['bot']

client = DiscordClient()
loop = client.loop


async def get_hystory():
    print('wait client ready')
    await client.ready.wait()
    print('client is ready')
    channels = client.channels
    # channels = {c.name: c for c in channels}
    print(channels)
    # print(fs.write_file('resources/channels.yaml', {c.name: c.id for c in channels}, 'yaml'))
    print('file saved')

loop.create_task(get_hystory())
client.run(TOKEN)
