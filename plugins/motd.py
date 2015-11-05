import subprocess
import re
import os
import random
from slackbot.bot import respond_to

@respond_to('motd', re.IGNORECASE)
def motd(message):
    # Take an ascii picutre / async?
    p1 = subprocess.Popen(["figlet", "ICN Engineering"], stdout=subprocess.PIPE).communicate()[0]
    p2 = subprocess.Popen(["fortune"], stdout=subprocess.PIPE)

    # select random cow
    cow = random.choice(os.listdir('/usr/share/cowsay/cows/'))

    p3 = subprocess.Popen(["cowsay", "-n", "-f", cow], stdin=p2.stdout, stdout=subprocess.PIPE).communicate()[0]

    motd = '```' + p1 + p3 + '```'

    message.reply(motd)
