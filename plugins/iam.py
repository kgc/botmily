from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import re

from botmily import irc

def iam(message_data, bot):
    if random.randint(0, 9) == 0:
	    msg = message_data['message']
	    if msg.find('im') != -1:
	    	idx = msg.find('im')
	    	bot.say(None,message_data['channel'],message_data['nick'] + ' is ' + msg[idx+3:])
	    elif msg.find("i'm") != -1:
	    	idx = msg.find("i'm")
	    	bot.say(None,message_data['channel'],message_data['nick'] + ' is ' + msg[idx+4:])


commands = {}
triggers = [("i'm ", iam),('im ',iam)]

