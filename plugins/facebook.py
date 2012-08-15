# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import re
from urllib import quote_plus
from urllib2 import urlopen

def hook(nick, ident, host, message, bot, channel):
    if re.match('\.f', message) is None:
        return

    result = urlopen('http://graph.facebook.com/search?q=' + quote_plus(message[3:].encode('utf-8')))
    json_data = json.load(result)
    for item in json_data['data']:
        if 'message' in item:
            return item['from']['name'] + ': ' + item['message'].replace('\n', ' ')[:200] + ' Profile Link: http://facebook.com/profile.php?id=' + item['id'] + '&v=wall'

