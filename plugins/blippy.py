from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re

from botmily import irc

def hook(nick, ident, host, message, bot, channel):
    if re.search('blippy', irc.clear(message)) is None:
        return None
    if random.randint(0, 9) == 0:
        return 'blippy owns'
    return None
