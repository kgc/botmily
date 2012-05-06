from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

class Bot(irc.IRCClient):
    def signedOn(self):
        self.join(b"#botmily")

    def joined(self, channel):
        self.say(b"#botmily", b"hello world")

class BotFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        p = Bot()
        p.factory = self
        return p

if __name__ == '__main__':
    f = BotFactory()
    reactor.connectTCP("irc.synirc.net", 6667, f)
    reactor.run()
