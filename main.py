from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from twisted.internet import protocol, reactor

from botmily import bot
from botmily import config

class BotFactory(protocol.ClientFactory):
    def __init__(self):
        print("Creating the BotFactory")

    def buildProtocol(self, addr):
        print("Connected")
        p = bot.Bot()
        p.factory = self
        return p

if __name__ == '__main__':
    print("Starting the bot")
    config.getConfig()
    f = BotFactory()
    print("Connecting...")
    reactor.connectTCP(config.server, 6667, f)
    reactor.run()
