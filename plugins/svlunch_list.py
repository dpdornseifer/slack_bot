import re
import requests
import datetime
from utilities import slackasciiterminal
from itertools import chain
from prettytable import PrettyTable
from slackbot.bot import settings
from slackbot.bot import respond_to


# global data storage
info_cache = {}


def flatten(items_list):
    """ chain several lists to one """
    return list(chain.from_iterable(items_list))


def gettable(items):
    """ print items in form of an ascii table """
    table = PrettyTable(["Item", "Description", "Price"])
    table.align["Item"] = "l"
    table.align["Description"] = "l"
    table.padding_width = 1

    for item in items:
        table.add_row([item['label'], item['description'], item['price']])
    return table


def getmenu_json(cafe_num):
    """ lookup the local cache if the today's menu is available otherwise get it from the web """
    global info_cache
    today = datetime.date.today()

    # if cache entry is older than 24 hours update it
    if 'last_update' not in info_cache or info_cache['last_update'] < today:
        cafe_response = requests.get(
            'http://legacy.cafebonappetit.com/api/2/menus?format=jsonp&cafe={!s}'.format(cafe_num))
        info_cache['json_rep'] = cafe_response.json()
        info_cache['last_update'] = today

    return info_cache['json_rep']


@respond_to('lunch (.*)', re.IGNORECASE)
def lunch(message, something):

    # internal mapping or sap cafes to ids
    def cafe_lookup(cafe_name):
        """ do the lookup of cafe names to the cafe bonappetit internal codes """
        return settings.CAFES.get(cafe_name, settings.CAFES_DEFAULT)

    cafe_num = cafe_lookup(something)

    cafe_json = getmenu_json(cafe_num)

    # a little bit of json processing to get the necessary information
    cafe_parts = cafe_json['days'][0]['cafes'][str(cafe_num)]
    cafe_dayparts = cafe_parts['dayparts'][0]
    cafe_stations = [i['stations'] for i in cafe_dayparts if i['label'] == 'Lunch']

    # filter out the grill std. items and focus on the menus
    cafe_items = flatten([i['items'] for i in cafe_stations[0] if
                          i['label'] != "grill" and
                          i['label'] != "market grill" and
                          i['label'] != "fire"])

    # lookup the items via their item id
    cafe_dayitems = cafe_json['items']

    # add the label, description and the price
    cafe_lunch_items = []
    for item in cafe_items:
        cafe_lunch_items.append({'label': cafe_dayitems[item]['label'][:30],
                                 'description': cafe_dayitems[item]['description'][:50],
                                 'price': cafe_dayitems[item]['price']})

    table = gettable(cafe_lunch_items)
    asciitable = slackasciiterminal(table.get_string())

    message.reply(asciitable)
