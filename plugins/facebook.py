# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import random
import re
from urllib import quote_plus
from urllib2 import urlopen

def facebook(message_data, bot):
    result = urlopen('http://graph.facebook.com/search?q=' + quote_plus(message_data["parsed"]))
    json_data = json.load(result)
    usable_results = []
    for item in json_data['data']:
        if 'message' in item:
            usable_results.append(item)
    item = random.choice(usable_results)
    return item['from']['name'] + ': ' + item['message'].replace('\n', ' ')[:200] + ' Profile Link: http://facebook.com/profile.php?id=' + item['id'] + '&v=wall'

commands = {"facebook": facebook, "ope": facebook}
triggers = []

