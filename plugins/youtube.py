from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import locale
import re
import time
from datetime import datetime, timedelta
from gdata.youtube import service

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
  

def hook(nick, ident, host, message):
    video_uri = re.search(regex, message, re.I)
    if video_uri is None:
        return None
    id = video_uri.group(1)
    youtube = service.YouTubeService()
    youtube.ssl = True
    entry = youtube.GetYouTubeVideoEntry(video_id=id)
    string = "\u0002"
    string += entry.media.title.text + "\u000f - length \u0002"
    string += convertHMS(entry.media.duration.seconds) + "\u000f - rated \u0002"
    string += locale.format("%.2f", float(entry.rating.average)) + "/5.0\u000f ("
    string += entry.rating.num_raters + ") - \u0002"
    string += locale.format("%d", float(entry.statistics.view_count), True) + "\u000f views - \u0002"
    string += entry.author[0].name.text + "\u000f on \u0002"
    string += time.strftime("%Y.%m.%d", time.strptime(entry.published.text, "%Y-%m-%dT%H:%M:%S.000Z"))
    return string
