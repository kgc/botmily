from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ConfigParser import ConfigParser

name = ''
server = ''
channels = []

def getConfig():
    global name
    global server
    global channels
    config = ConfigParser()
    config.read('config.ini')
    name = config.get('main', 'name')
    server = config.get('main', 'server')
    channels = config.get('main', 'channels').split(" ")
    print("I will use the name: " + name)
    print("I will connect to the server: " + server)
    print("I will connect to the channels: " + ", ".join(channels))
