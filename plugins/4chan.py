# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

import imgur
import makeMacro

def fourchan(message_data, bot):
    board = ''
    if message_data['command'] == "anime":
        board = "/a/"
    if message_data['command'] == "dick":
        board = "/d/"

    result = urlopen('http://boards.4chan.org' + board)
    soup = BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    images = soup.findAll('a', attrs={'class': 'fileThumb'})
    url = 'http:' + random.choice(images)['href']
    if message_data['parsed'] != "":
        makeMacro.makeMacro(url, message_data['parsed'], "temp.jpg")
        url = imgur.postToImgur(str("temp.jpg"))
    return url

commands = {"anime": fourchan, "dick": fourchan}
triggers = []

