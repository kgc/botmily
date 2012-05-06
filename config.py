from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ConfigParser import ConfigParser

def getConfig():
    config = ConfigParser()
    config.read('config.ini')
    name = config.get('main', 'name')
    server = config.get('main', 'server')
    channels = config.get('main', 'channels')
    return name, server, channels
