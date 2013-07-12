from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ConfigParser import ConfigParser

name = ''
server = ''
channels = []
password = ''
tumblr_blog = ''
tumblr_user = ''
tumblr_password = ''
tumblr_title = ''
tumblr_tumbling = False
wolframalpha_api_key = ''
lastfm_api_key = ''

def getConfig():
    global name
    global server
    global channels
    global password
    global tumblr_blog
    global tumblr_user
    global tumblr_password
    global tumblr_title
    global tumblr_tumbling
    global wolframalpha_api_key
    global lastfm_api_key
    global oauth_token
    global oauth_secret
    global consumer_key
    global consumer_secret
    config = ConfigParser()
    config.read('config.ini')
    name = config.get('main', 'name')
    server = config.get('main', 'server')
    channels = config.get('main', 'channels').split(" ")
    password = config.get('main', 'password')
    tumblr_tumbling = config.getboolean('tumblr','tumbling')
    tumblr_blog = config.get('tumblr', 'blog')
    tumblr_user = config.get('tumblr' , 'user')
    tumblr_password = config.get('tumblr', 'password')
    tumblr_title = config.get('tumblr','post_titles')
    wolframalpha_api_key = config.get('wolframalpha', 'api_key')
    lastfm_api_key = config.get('lastfm', 'api_key')
    oauth_token = config.get('twitter', 'oauth_token')
    oauth_secret = config.get('twitter', 'oauth_secret')
    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')
    print("I will use the name: " + name)
    print("I will connect to the server: " + server)
    print("I will connect to the channels: " + ", ".join(channels))
