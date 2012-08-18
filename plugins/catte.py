# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import urllib2

def catte(message_data, bot):
    try:
        result = urllib2.urlopen('http://cattes.me:3333/random')
    except urllib2.URLError:
        return 'No cattes :('
    return 'http://cattes.me:3333/images/' + result.read()

commands = {"catte": catte}
triggers = []

