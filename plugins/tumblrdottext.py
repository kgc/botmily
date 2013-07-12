from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from twitter import Twitter
from twitter import OAuth
from botmily import config
import random
#randomly return one of the last 200 tweets from https://twitter.com/TumblrTXT
#rate limit is 300 requests per 15 minutes
def tumblr(message_data, bot):
    t = Twitter(api_version=1.1, auth=OAuth(config.oauth_token,
    config.oauth_secret, config.consumer_key, config.consumer_secret))
    tweetno = random.randint(0,199)
    tweet = t.statuses.user_timeline.tumblrtxt(count=200)[tweetno]
    return tweet['text']


commands = {"tumblr": tumblr}
triggers = []

