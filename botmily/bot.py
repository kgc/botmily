from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pkgutil
import re

from twisted.words.protocols import irc

from botmily import config
import plugins

class Bot(irc.IRCClient):
    def __init__(self):
        self.nickname = config.name
        self.realname = b"Botmily https://github.com/kgc/botmily"
        self.channels = config.channels

        print("Initializing hooks...")
        self.hooks = []
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
            print("Loading plugin " + modname)
            plugin = __import__("plugins." + modname, fromlist="hook")
            self.hooks.append(plugin.hook)

    def signedOn(self):
        print("Signed on to the IRC server")
        for channel in self.channels:
            self.join(str(channel))

    def joined(self, channel):
        print("Joined channel " + channel)

    def privmsg(self, user, channel, message):
        for function in self.hooks:
            output = function(user, message)
            if output is not None:
                self.say(channel, output.encode("utf-8"))
