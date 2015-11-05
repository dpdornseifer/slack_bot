from slackbot.bot import listen_to
from slackbot.bot import respond_to
from bot_utilities import Command
import re

@respond_to('ascii pic', re.IGNORECASE)
def takepic(message):
    # Take an ascii picutre / async?
    command = Command("ping 8.8.8.8")
    command.run(timeout=3)

    # Read from the file
    with open('pic.txt', 'r') as picfile:
        picture = '```' + picfile.read() + '```'
    # reply
    message.reply(picture)
