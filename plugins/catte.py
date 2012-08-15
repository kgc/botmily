# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen

def catte(message_data, bot):
    result = urlopen('http://cattes.me:3333/random')
    return 'http://cattes.me:3333/images/' + result.read()

commands = {"catte": catte}
triggers = []

