from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pkgutil
import re
import sys

from twisted.words.protocols import irc

from botmily import config
import plugins

def splituser(user):
    nick, remainder = user.split('!', 1)
    ident, host = remainder.split('@', 1)
    return nick, ident, host

class Bot(irc.IRCClient):
    def __init__(self):
        self.nickname = config.name
        self.realname = b"Botmily https://github.com/kgc/botmily"
        self.channels = config.channels

        print("Initializing plugins...")
        self.commands = {}
        self.triggers = []
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
            print("Loading plugin " + modname)
            plugin = __import__("plugins." + modname, fromlist="hook")
            self.commands.update(plugin.commands)
            self.triggers.extend(plugin.triggers)

    def signedOn(self):
        print("Signed on to the IRC server")
        for channel in self.channels:
            self.join(str(channel))

    def joined(self, channel):
        print("Joined channel " + channel)

    def privmsg(self, user, channel, message):
        nick, ident, host = splituser(user)
        message_data = {"nick":    nick,
                        "user":    user,
                        "host":    host,
                        "channel": channel,
                        "message": unicode(message, encoding='utf-8')}
        command_match = re.match("\.([^ ]+) ?(.*)", message_data["message"])
        if command_match is not None:
            sent_command = command_match.group(1)
            message_data["parsed"] = command_match.group(2)
            possible_commands = []
            for command, function in self.commands.iteritems():
                if sent_command == command:
                    possible_commands = [(command, function)]
                    break
                if command.find(sent_command) == 0:
                    possible_commands.append((command, function))
            if len(possible_commands) == 1:
                message_data["command"] = possible_commands[0][0]
                output = possible_commands[0][1](message_data, self)
                self.say(nick, channel, output)
            if len(possible_commands) > 1:
                commands_formatted = []
                for command, function in possible_commands:
                    commands_formatted.append("." + command)
                self.say(nick, channel, "Did you mean: " + ",".join(commands_formatted) + "?")
        for tup in self.triggers:
            trigger, function = tup
            if re.search(trigger, message_data["message"]) is not None:
                message_data["re"] = re.search(trigger, message_data["message"])
                output = function(message_data, self)
                self.say(nick, channel, output)

    def say(self, nick, channel, output):
        if output is None:
            return
        if self.nickname == channel:
            self.msg(str(nick), output.encode("utf-8"))
        else:
            self.msg(channel, str(nick) + str(": ") + output.encode("utf-8"))

