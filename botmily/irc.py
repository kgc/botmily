from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import asynchat
import time
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

def split_prefix(prefix):
    nick, remainder = prefix[1:].split(b"!", 1)
    user, host = remainder.split(b"@", 1)
    return nick, user, host

class irc_handler(asynchat.async_chat):
    def __init__(self, sock, bot):
        asynchat.async_chat.__init__(self, sock=sock)
        self.ibuffer = b""
        self.set_terminator(b"\r\n")
        self.bot = bot
        self.push(b"NICK %s\r\n" %bot.nickname)
        self.push(b"USER botmily 0 0 :Botmily\r\n")

    def collect_incoming_data(self, data):
        self.ibuffer += data

    def found_terminator(self):
        current_line = self.ibuffer
        self.ibuffer = b""
        prefix = None
        if current_line[0] == b":":
            prefix, null, current_line = current_line.partition(b" ")
        command, null, params = current_line.partition(b" ")
        if b":" in params:
            other_params, null, trailing = params.partition(b":")
            if len(other_params) == 0:
                params = [trailing]
            else:
                params = other_params.split(" ") + [trailing]
        else:
            params = params.split(" ")
        if command[0] >= b"0" and command[0] <= b"9":
            if command == b"001":
                for channel in self.bot.channels:
                    self.join(str(channel))
        else:
            try:
                handler = getattr(self, "raw_" + command)
            except AttributeError:
                return
            handler(prefix, params)

    def join(self, channel):
        self.push(b"JOIN " + channel + b"\r\n")

    def part(self, channel):
        self.push(b"PART " + channel + b"\r\n")

    def kick(self, channel, user):
        self.push(b"KICK " + str(channel) + b" " + str(user) + b"\r\n")

    def privmsg(self, receiver, message):
        self.push(b"PRIVMSG " + str(receiver) + b" :" + message.encode("utf-8") + b"\r\n")

    def notice(self, receiver, message):
        self.push(b"NOTICE " + str(receiver) + b" :" + message.encode("utf-8") + b"\r\n")

    def pong(self, message):
        self.push(b"PONG " + message + b"\r\n")

    def raw_PRIVMSG(self, prefix, params):
        nick, user, host = split_prefix(prefix)
        channel = params[0]
        message = params[-1].decode("utf-8")
        self.bot.privmsg(nick, user, host, channel, message)

    def raw_PING(self, prefix, params):
        self.pong(params[0])

    def raw_JOIN(self, prefix, params):
        self.bot.join(params[0])

