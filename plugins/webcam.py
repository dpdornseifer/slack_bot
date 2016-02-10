from slackbot.bot import respond_to
from utilities import Command, slackasciiterminal
import re

@respond_to('ascii pic', re.IGNORECASE)
def takepic(message):
    # Take an ascii picutre / async?
    command = Command("ping 8.8.8.8")
    command.run(timeout=3)

    # Read from the file
    with open('pic.txt', 'r') as picfile:
        asciipicture = slackasciiterminal(picfile.read())
    # reply
    message.reply(asciipicture)
