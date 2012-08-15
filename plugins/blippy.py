from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re

from botmily import irc

def blippy(message_data, bot):
    if random.randint(0, 9) == 0:
        return 'blippy owns'

commands = {}
triggers = [("blippy", blippy)]

