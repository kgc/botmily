# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random

def hn(message_data, bot):
    hack_list = []
    f = open("hn.txt", "r")
    current_hack = ""
    for line in f:
        if line == "%\n":
            hack_list.append(current_hack)
            current_hack = ""
        else:
            current_hack += line
    return random.sample(hack_list, 1)[0]

commands = {"hn": hn}
triggers = []

