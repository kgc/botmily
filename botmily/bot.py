from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from twisted.words.protocols import irc

from botmily import config
from plugins import fml

class Bot(irc.IRCClient):
    def __init__(self):
        self.nickname = config.name
        self.realname = b"Botmily https://github.com/kgc/botmily"
        self.channels = config.channels

    def signedOn(self):
        print("Signed on to the IRC server")
        for channel in self.channels:
            self.join(str(channel))

    def joined(self, channel):
        print("Joined channel " + channel)

    def privmsg(self, user, channel, message):
        if re.match('.fml', message) is not None:
            self.say(channel, fml.fml())
        if re.search('im gay', message) is not None:
            self.say(channel, b"same")
        if re.search('blippy', message) is not None:
            self.say(channel, b"blippy owns")
