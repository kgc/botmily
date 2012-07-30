# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

def hook(nick, ident, host, message, bot, channel):
    if re.match('\.et', message) is None:
        return None

    result = urlopen('http://www.etymonline.com/index.php?term=' + message[4:])
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    return "".join(soup.dl.findAll(text=True)).replace("\n", " ")
