from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import locale
import re
import time
from datetime import datetime, timedelta
from gdata.youtube import service

from botmily import irc

regex = r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)([-_a-z0-9]+)'

def convertHMS(secs):
    sec = timedelta(seconds=int(secs))
    d = datetime(1,1,1) + sec
    if d.day-1 > 0:
        return '%d days %d hours %d minutes %d seconds' %(d.day-1,d.hour,d.minute,d.second)
    elif d.hour > 0:
        return '%d hours %d minutes %d seconds' %(d.hour,d.minute,d.second)
    elif d.minute > 0:
        return '%d minutes %d seconds' %(d.minute,d.second)
    else:   
        return '%d seconds' %d.second 
  
def search(message_data, bot):
    yt_service = service.YouTubeService()
    query = service.YouTubeVideoQuery()
    query.vq = message_data["parsed"]
    query.orderby = 'relevance'
    query.racy = 'include'
    feed = yt_service.YouTubeQuery(query)
    title = feed.entry[0].title.text
    link = feed.entry[0].link[0].href
    return "\u0002%s\u000f - %s" %(title , link)

def parse(message_data, bot):
    id = message_data["re"].group(1)
    youtube = service.YouTubeService()
    youtube.ssl = True
    entry = youtube.GetYouTubeVideoEntry(video_id=id)
    string = irc.bold(unicode(entry.media.title.text, encoding='utf-8')) + " - length "
    string += irc.bold(convertHMS(entry.media.duration.seconds)) + " - rated "
    if entry.rating is not None:
        string += irc.bold(locale.format("%.2f", float(entry.rating.average))) + "/5.0 ("
        string += entry.rating.num_raters + ") - "
    if entry.statistics is not None:
        string += irc.bold(locale.format("%d", float(entry.statistics.view_count), True)) + " views - "
    string += irc.bold(unicode(entry.author[0].name.text, encoding='utf-8')) + " on "
    string += irc.bold(time.strftime("%Y.%m.%d", time.strptime(entry.published.text, "%Y-%m-%dT%H:%M:%S.000Z")))
    return string

commands = {"yt": search, "youtube": search}
triggers = [(regex, parse)]

