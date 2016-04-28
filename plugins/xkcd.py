import re
import datetime
import requests
import random
from slackbot.bot import respond_to

info_cache = {}


def get_current_number():

    today = datetime.date.today()
    global info_cache

    if 'last_update' not in info_cache or info_cache['last_update'] < today:
        response = requests.get('http://xkcd.com/info.0.json')
        num = response.json()['num']
        info_cache['num'] = num
        info_cache['last_update'] = today

    return info_cache['num']


@respond_to('xkcd$', re.IGNORECASE)
def xkcd2(message):
    """ method overloading to have just one parameter """
    xkcd1(message, 'latest')


@respond_to('xkcd (.*)', re.IGNORECASE)
def xkcd1(message, something):

    if something == 'random':
        """ get random xkcd by picking a number between 1 and n """
        para = str(random.randrange(1, get_current_number())) + '/'

    elif something.isdigit():
        """ get specific xkcd number """

        if int(something) > get_current_number():
            para = ''
        else:
            para = something + '/'
    else:
        para = ''

    url = 'http://xkcd.com/{}info.0.json'.format(para)
    response = requests.get(url)
    response_json = response.json()
    img = response_json['img']
    alt = response_json['alt']

    message.reply(img)
    message.reply(alt)
