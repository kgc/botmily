from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from botmily import ircify

def hook(nick, ident, host, message, bot, channel):
    if re.search('check your .*privilege', ircify.ircify(message), re.I) is None:
        return None
    bot.kick(str(channel), str(nick));
    return 'out'
