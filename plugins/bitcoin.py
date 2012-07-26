from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re
import json
import urllib2

from botmily import ircify
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

def hook(nick, ident, host, message, bot, channel):
    if re.match('\.bit', message) is not None:
        tick = get_btc_price()
        return "Current price: \u00037$" + str(tick['last']) + "\u000f - High: \u00037$" + str(tick['high']) + "\u000f - Low: \u00037$" + str(tick['low']) + "\u000f - Volume: " + str(tick['volume']) + "BTC"

    money = re.search(regex1, message, re.I)
    if money is None:
        money = re.search(regex2,message,re.I)
        if money is None:
            return None
        else:
            amount = float(money.group(1))
    else:
        amount = float(money.group(1))
    avg = get_btc_price()['average']
    return '%s if you converted that to bitcoins you could have %f BTC!' %(nick , (amount / avg))

