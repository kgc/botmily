from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

import config
import fml

class Bot(irc.IRCClient):
    def __init__(self, name, channels):
        self.nickname = name
        self.realname = b"Botmily https://github.com/kgc/botmily"
        self.channels = channels

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

class BotFactory(protocol.ClientFactory):
    def __init__(self, name, channels):
        self.name = name
        self.channels = channels

    def buildProtocol(self, addr):
        p = Bot(self.name, self.channels)
        p.factory = self
        return p

if __name__ == '__main__':
    print("Starting the bot")
    name, server, channels = config.getConfig()
    f = BotFactory(name, channels.split(" "))
    reactor.connectTCP(server, 6667, f)
    reactor.run()
