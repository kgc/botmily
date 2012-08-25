# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib import quote_plus
from urllib2 import urlopen
from xml.etree import ElementTree

from botmily import config
from botmily import irc

def lastfm(message_data, bot):
    if message_data["parsed"] == "":
        return "Type in a username ¬_¬"
    result = urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + quote_plus(message_data["parsed"]) + '&api_key=' + config.lastfm_api_key)
    root = ElementTree.fromstring(result.read())
    track = root.find('recenttracks/track')
    result_string = irc.bold(message_data["parsed"]) + '\'s last track - '
    result_string += irc.bold(track.find('name').text) + ' :: Artist - '
    result_string += irc.bold(track.find('artist').text) + ' :: Link to Song - '
    result_string += irc.bold(track.find('url').text)
    return result_string

commands = {"lastfm": lastfm}
triggers = []

