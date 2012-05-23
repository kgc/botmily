from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ConfigParser import ConfigParser

name = ''
server = ''
channels = []
tumblr_blog = ''
tumblr_user = ''
tumblr_password = ''
tumblr_title = ''
tumblr_tumbling = False

def getConfig():
    global name
    global server
    global channels
    global tumblr_blog
    global tumblr_user
    global tumblr_password
    global tumblr_title
    global tumblr_tumbling
    config = ConfigParser()
    config.read('config.ini')
    name = config.get('main', 'name')
    server = config.get('main', 'server')
    channels = config.get('main', 'channels').split(" ")
    tumblr_tumbling = config.getboolean('tumblr','tumbling')
    tumblr_blog = config.get('tumblr', 'blog')
    tumblr_user = config.get('tumblr' , 'user')
    tumblr_password = config.get('tumblr', 'password')
    tumblr_title = config.get('tumblr','post_titles')
    print(tumblr_tumbling)
    print("I will use the name: " + name)
    print("I will connect to the server: " + server)
    print("I will connect to the channels: " + ", ".join(channels))
