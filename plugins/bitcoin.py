from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re
import json
import urllib2

from botmily import irc

regex1 = r'\$([0-9]+\.?[0-9][0-9]?)'
regex2 = r".*?(\d+\.?\d\d)[     ]*dolla"

def get_btc_price():
    response = urllib2.urlopen('https://mtgox.com/api/1/BTCUSD/ticker')
    tick = json.loads(response.read())['return']
    data = {}
    data['average'] = float(tick['avg']['value'])
    data['low'] = float(tick['low']['value'])
    data['high'] = float(tick['high']['value'])
    data['last'] = float(tick['last']['value'])
    data['volume'] = float(tick['vol']['value'])
    return data

def btc_price(message_data, bot):
    try:
        tick = get_btc_price()
    except urllib2.URLError:
        return "MtGox is down :("
    return "Current price: $" + irc.color(str(tick['last']), 'orange') + " - High: $" + irc.color(str(tick['high']), 'orange') + " - Low: $" + irc.color(str(tick['low']), 'orange') + " - Volume: " + str(tick['volume']) + "BTC"

def btc_convert(message_data, bot):
    if random.randint(0, 9) != 0:
        return
    amount = float(message_data["re"].group(1))
    avg = get_btc_price()['average']
    return 'If you converted that to bitcoins you could have %f BTC!' %((amount / avg))

commands = {"bitcoin": btc_price, "btc": btc_price}
triggers = [(regex1, btc_convert), (regex2, btc_convert)]

