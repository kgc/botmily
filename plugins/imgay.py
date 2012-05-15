from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

def hook(nick, ident, host, message):
    if re.search('im gay', message) is None:
        return None
    return 'same'
