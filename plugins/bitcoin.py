from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re
import json
import urllib

from botmily import ircify
regex1 = r'\$([0-9]+\.?[0-9][0-9]?)'
regex2 = r".*?(\d+\.?\d\d)[     ]*dolla"



def hook(nick, ident, host, message, bot, channel):
    money = re.search(regex1, message, re.I)
    if money is None:
        money = re.search(regex2,message,re.I)
        if money is None:
            return None
        else:
            amount = float(money.group(1))
    else:
        amount = float(money.group(1))
    response = urllib.urlopen('https://mtgox.com/api/1/BTCUSD/ticker')
    tick = json.loads(response.read())['return']
    avg = float(tick['avg']['value'])
    return '%s if you converted that to bitcoins you could have %f BTC!' %(nick , (amount / avg))
     