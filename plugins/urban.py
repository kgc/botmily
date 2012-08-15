# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

def urban(message_data, bot):
    result = urlopen('http://www.urbandictionary.com/define.php?term=' + message_data["parsed"])
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    definition = soup.find('div', attrs={'class': 'definition'})
    return definition.text

commands = {"urban": urban}
triggers = []

