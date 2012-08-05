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

def hook(nick, ident, host, message, bot, channel):
    if re.match('\.last', message) is None:
        return None

    query = message[6:]
    result = urlopen('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + quote_plus(query.encode('utf-8')) + '&api_key=' + config.lastfm_api_key)
    root = ElementTree.fromstring(result.read())
    track = root.find('recenttracks/track')
    result_string = irc.bold(query) + '\'s last track - '
    result_string += irc.bold(track.find('name').text) + ' :: Artist - '
    result_string += irc.bold(track.find('artist').text) + ' :: Link to Song - '
    result_string += irc.bold(track.find('url').text)
    return result_string

