# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

def etymology(message_data, bot):
    result = urlopen('http://www.etymonline.com/index.php?term=' + message_data["parsed"])
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    if soup.dl is None:
        return "Not found"
    return "".join(soup.dl.findAll(text=True)).replace("\n", " ")

commands = {"etymology": etymology}
triggers = []

