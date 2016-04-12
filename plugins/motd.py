import subprocess
import re
import os
import random
from utilities import slackasciiterminal
from slackbot.bot import settings
from slackbot.bot import respond_to

@respond_to('motd', re.IGNORECASE)
def motd(message):

    try:
        team_name = settings.TEAM_NAME if settings.TEAM_NAME is not None else 'Team Channel'
    except ImportError:
        pass

    # generate the ascii arts
    p1 = subprocess.Popen(["figlet", team_name], stdout=subprocess.PIPE,).communicate()[0]
    p2 = subprocess.Popen(["fortune", "-a"], stdout=subprocess.PIPE,)

    # select random cow
    cow = random.choice(os.listdir('/usr/share/cowsay/cows/'))
    p3 = subprocess.Popen(["cowsay", "-n", "-f", cow], stdin=p2.stdout, stdout=subprocess.PIPE,).communicate()[0]

    # put together the motd
    motd = slackasciiterminal(p1 + str(p3))

    message.reply(motd)
