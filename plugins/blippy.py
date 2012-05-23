from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re

def hook(nick, ident, host, message):
    if re.search('blippy', message) is None:
        return None
    if random.randint(0, 9) == 0:
        return 'blippy owns'
    return None
