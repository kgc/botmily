from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unicodedata

controls = {'bold':  '\u0002',
            'color': '\u0003',
            'clear': '\u000f'}

colors = {'white':        '00',
          'black':        '01',
          'blue':         '02',
          'green':        '03',
          'red':          '04',
          'brown':        '05',
          'purple':       '06',
          'orange':       '07',
          'yellow':       '08',
          'light green':  '09',
          'teal':         '10',
          'light cyan':   '11',
          'light blue':   '12',
          'pink':         '13',
          'grey':         '14',
          'light grey':   '15'}

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
