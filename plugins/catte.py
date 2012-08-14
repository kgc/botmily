# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen

def hook(nick, ident, host, message, bot, channel):
    if re.match('\.catte', message) is None:
        return

    result = urlopen('http://cattes.me:3333/random')
    return 'http://cattes.me:3333/images/' + result.read()
