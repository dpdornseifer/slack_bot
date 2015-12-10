import re
import requests
from itertools import chain
from prettytable import PrettyTable
from slackbot.bot import respond_to


def flatten(items_list):
    return list(chain.from_iterable(items_list))


def gettable(items):
    table = PrettyTable(["Item", "Description", "Price"])
    table.align["Item"] = "l"
    table.align["Description"] = "l"
    table.padding_width = 1

    for item in items:
        table.add_row([item['label'], item['description'], item['price']])
    return table


@respond_to('lunch (.*)', re.IGNORECASE)
def svlunch(message, something):
    # internal mapping or sap cafes to ids
    def cafe_lookup(cafe):
        return {
            'cafe_1': 246,
            'cafe_3': 245,
            'cafe_8': 247
        }.get(cafe, 246)

    cafe = cafe_lookup(something)
    cafe_response = requests.get('http://legacy.cafebonappetit.com/api/2/menus?format=jsonp&cafe={!s}'.format(cafe))
    cafe_json = cafe_response.json()

    # a little bit of json processing to get the necessary information
    cafe_parts = cafe_json['days'][0]['cafes'][str(cafe)]


    cafe_name = cafe_parts['name']
    cafe_dayparts = cafe_parts['dayparts'][0]

    cafe_stations = [i['stations'] for i in cafe_dayparts if i['label'] == 'Lunch']

    # filter out the grill std. items
    cafe_items = flatten([i['items'] for i in cafe_stations[0] if
                          i['label'] != "grill" and
                          i['label'] != "market grill" and
                          i['label'] != "fire"])

    # lookup the items via their item id
    cafe_dayitems = cafe_json['items']

    # add the label, description and the price
    cafe_lunch_items = []
    for item in cafe_items:
        cafe_lunch_items.append({'label': cafe_dayitems[item]['label'], 'description': cafe_dayitems[item]['description'][0:50], 'price':cafe_dayitems[item]['price']})

    table = gettable(cafe_lunch_items)

    asciitable = '```' + table.get_string() + '```'

    message.reply(asciitable)
