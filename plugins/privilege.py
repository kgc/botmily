from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from botmily import irc

def privilege(message_data, bot):
    bot.kick(str(message_data["channel"]), str(message_data["nick"]));
    return 'out'

commands = {}
triggers = [("check your .*privilege", privilege)]

