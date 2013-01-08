# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import urllib2

from BeautifulSoup import BeautifulStoneSoup

from botmily import irc

def steam(message_data, bot):
    try:
        result = urllib2.urlopen('http://www.steamcalculator.com/id/' + message_data["parsed"])
    except urllib2.URLError:
        return "Nothing found sorry"
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    data = soup.find('div', id='rightdetail')
    game_count = re.search('Found ([0-9]+)', data.text).group(1)
    output = irc.bold(message_data["parsed"]) + ' owns ' + irc.bold(game_count) + ' Games with a value of ' + irc.bold(re.search('\$.*', data.text).group(0)) + '.'
    if int(game_count) >= 125:
        output += ' <--- jesus fuck quit buying games you neckbeard.'
    return output

commands = {"sc": steam, "steamcalc": steam}
triggers = []

