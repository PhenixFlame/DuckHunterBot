from secret import settings
import yaml

example_settings_ = {
    "bot": {
        "TOKEN": "BOT_TOKEN",  # this for DuckHunterBot#3729 from
        "BOTFLAG": True,
        "GUILD": 'GUILD_NAME',
        "CHANNEL": 'CHANNEL_NAME',
        "DuckHuntBotName": "DUCK_HUNT_BOT_NAME",
        "SelfName": "MY_BOT_NAME"
    },
    "user_test": {
        "TOKEN": "USER_TOKEN",
        "BOTFLAG": False,
        "GUILD": 'TEST_GUILD_NAME',
        "CHANNEL": 'TEST_CHANNEL_NAME',
        "DuckHuntBotName": "DUCK_HUNT_BOT_NAME",
        "SelfName": "MY_USER_NAME"
    },
    "user": {
        "TOKEN": "USER_TOKEN",
        "BOTFLAG": False,
        "GUILD": 'GUILD_NAME',
        "CHANNEL": 'CHANNEL_NAME',
        "DuckHuntBotName": "DUCK_HUNT_BOT_NAME",
        "SelfName": "MY_USER_NAME"
    }

}

# ____________CONSTANTS________________
# bot mode
CONFIG = settings['bot']
# CONFIG = settings['user_test']
# CONFIG = settings['user']

# channels settings
TOKEN = CONFIG['TOKEN']
BOTFLAG = CONFIG['BOTFLAG']
GUILD_HUNT = CONFIG["GUILD"]
CHANNEL_HUNT = CONFIG["CHANNEL"]

# event constants
SELF_NAME = CONFIG["SelfName"]
DUCK_HUNT_BOT_NAME = CONFIG["DuckHuntBotName"]

EVENTS = yaml.safe_load(open('resources/EVENTS.yaml', 'r'))
DECISION_TREE = yaml.safe_load(open('resources/DECISION_TREE.yaml', 'r'))
# ____________END_CONSTANTS____________

