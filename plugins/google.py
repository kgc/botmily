# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import random
import re
from urllib import quote_plus
from urllib2 import urlopen

from BeautifulSoup import BeautifulStoneSoup

from botmily import irc

def google(message_data, bot):
    result = urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&safe=off&q=' + quote_plus(message_data["parsed"].encode("utf-8")))
    json_data = json.load(result)
    if len(json_data["responseData"]["results"]) == 0:
        return "No results found"
    first_result = json_data['responseData']['results'][0]
    output = first_result['unescapedUrl'] + ' | '
    output += irc.bold(BeautifulStoneSoup(first_result['titleNoFormatting'], convertEntities=BeautifulStoneSoup.HTML_ENTITIES).text) + ' | '
    output += BeautifulStoneSoup(first_result['content'], convertEntities=BeautifulStoneSoup.HTML_ENTITIES).text
    return output

def gis(message_data, bot):
    result = urlopen('http://ajax.googleapis.com/ajax/services/search/images?v=1.0&safe=off&q=' + quote_plus(message_data["parsed"].encode("utf-8")))
    json_data = json.load(result)
    if len(json_data["responseData"]["results"]) == 0:
        return "No results found"
    chosen_result = random.choice(json_data["responseData"]["results"][:10])
    return chosen_result["unescapedUrl"]

commands = {"g": google, "google": google, "gis": gis}
triggers = []

