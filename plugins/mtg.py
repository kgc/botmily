# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib import quote_plus
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

def mtg(message_data, bot):
    result = urlopen('http://magiccards.info/query?v=card&s=cname&q=' + quote_plus(message_data["parsed"]))
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    card = soup.findAll('table', align='center')[1]
    output = card.find('a').text + ' | '
    output += card.find('p').text.strip().replace('\n', ' ') + ' | '
    output += card.find('p', attrs={'class': 'ctext'}).text + ' | '
    output += card.find('small').findAll('b')[1].text + ' | '
    output += 'http://magiccards.info' + card.find('a')['href']
    return output

commands = {"mtg": mtg}
triggers = []

