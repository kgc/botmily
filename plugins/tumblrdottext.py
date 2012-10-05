from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from twitter import Twitter
import random
#randomly return one of the last 50 tweets from https://twitter.com/TumblrTXT
def tumblr(message_data, bot):
    t = Twitter()
    tweetno = random.randint(0,49)
    tweet = t.statuses.user_timeline.tumblrtxt(count=50)[tweetno]
    return tweet['text']


commands = {"tumblr": tumblr}
triggers = []

