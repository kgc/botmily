from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unicodedata

controls = {'bold':  '\u0002',
            'color': '\u0003',
            'clear': '\u000f'}

colors = {'white':        '0',
          'black':        '1',
          'blue':         '2',
          'green':        '3',
          'red':          '4',
          'brown':        '5',
          'purple':       '6',
          'orange':       '7',
          'yellow':       '8',
          'light green':  '9',
          'teal':        '10',
          'light cyan':  '11',
          'light blue':  '12',
          'pink':        '13',
          'grey':        '14',
          'light grey':  '15'}

def clear(message):
    new_string = ''
    for character in message:
        if unicodedata.category(character) != 'Cc':
            new_string += character
    return new_string

def bold(message):
    return controls['bold'] + message + controls['clear']

def color(message, color):
    return controls['color'] + colors[color] + message + controls['clear']
