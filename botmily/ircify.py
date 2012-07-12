from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unicodedata

def ircify(message):
    new_string = ''
    for character in message:
        if unicodedata.category(character) != 'Cc':
            new_string += character
    return new_string
