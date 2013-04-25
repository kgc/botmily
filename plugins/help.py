# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def help(message_data, bot):
    helpmsg = 'Currently available commands are : '
    for key in bot.commands:
    	helpmsg = helpmsg + str(key) + ' '
    return helpmsg

commands = {"help": help}
triggers = []

