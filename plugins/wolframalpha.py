# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib import quote_plus
from urllib2 import urlopen
from xml.etree import ElementTree

from botmily import config

def wa(message_data, bot):
    result = urlopen('http://api.wolframalpha.com/v2/query?format=plaintext&input=' + quote_plus(message_data["parsed"]) + '&appid=' + config.wolframalpha_api_key)
    root = ElementTree.fromstring(result.read())
    pods = root.findall('pod')
    result_string = ''
    for pod in pods:
        if pod.get('id') != 'Input' and pod.findtext('subpod/plaintext') != '':
            result_string += pod.get('title') + ': ' + pod.findtext('subpod/plaintext').strip().replace('\n', ' ') + '. '
    return result_string

commands = {"wa": wa}
triggers = []

