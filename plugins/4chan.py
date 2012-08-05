# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

def hook(nick, ident, host, message, bot, channel):
    board = ''
    if re.match('\.anime', message) is not None:
        board = '/a/'
    if re.match('\.dick', message) is not None:
        board = '/d/'
    if board == '':
        return

    result = urlopen('http://boards.4chan.org' + board)
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    images = soup.findAll('a', attrs={'class': 'fileThumb'})
    return 'http:' + random.choice(images)['href']
