from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

def hook(nick, message):
    if re.search('blippy', message) is None:
        return None
    return 'blippy owns'
