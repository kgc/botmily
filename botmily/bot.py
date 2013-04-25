from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import asyncore
import pkgutil
import re
import socket
import sys
import traceback

from botmily import config
from botmily import irc
import plugins

class bot():
	def __init__(self):
		self.server = config.server
		self.nickname = config.name
		self.realname = b"Botmily https://github.com/kgc/botmily"
		self.channels = config.channels
		self.password = config.password

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.server, 6667))
		self.irc = irc.irc_handler(self.socket, self , self.irc_error)

		print("Initializing plugins...")
		self.commands = {}
		self.triggers = []
		for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
			print("Loading plugin " + modname)
			plugin = __import__("plugins." + modname, fromlist="hook")
			self.commands.update(plugin.commands)
			self.triggers.extend(plugin.triggers)

		asyncore.loop()

	def join(self, nick, user, host, channel):
		if nick == self.nickname:
			print("Joined channel " + channel)

	def privmsg(self, nick, user, host, channel, message):
		message_data = {"nick":    nick,
		                "user":    user,
		                "host":    host,
		                "channel": channel,
		                "message": message}
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
				try:
					output = possible_commands[0][1](message_data, self)
					self.say(nick, channel, output)
				except Exception, E:
					print('Encountered error while processing commmand %s with input %s' %(str(possible_commands[0][1]),str(message_data)))
					traceback.print_exc()
					self.say(nick,channel,'I crashed while trying to deal with something you said @_@')

			if len(possible_commands) > 1:
				commands_formatted = []
				for command, function in possible_commands:
					commands_formatted.append("." + command)
				self.say(nick, channel, "Did you mean: " +
				                        ",".join(commands_formatted) + "?")
		for tup in self.triggers:
			trigger, function = tup
			if re.search(trigger, message_data["message"], re.I) is not None:
				message_data["re"] = re.search(trigger,
				                               message_data["message"], re.I)
				try:
					output = function(message_data, self)
					self.say(nick, channel, output)
				except Exception, E:
					print('Encountered error while processing trigger %s with input %s' %(str(function),str(message_data)))
					traceback.print_exc()
					self.say(nick,channel,'I crashed while trying to deal with something you said @_@')
				

	def say(self, nick, channel, output):
		if output is None:
			return
		if self.nickname == channel:
			self.irc.privmsg(nick, output)
		else:
			self.irc.privmsg(channel, nick + ": " + output)

	def irc_error(self):
		print('Nasty error caught, trying to continue anyway , details below :  ')
		traceback.print_exc()