from __future__ import division
from __future__ import unicode_literals

import re
from botmily import config
from botmily.db import db
import achievChecks , tumble

def checkAchievs(nick , host , message):
    results = ''
    for x in dir(achievChecks):
        if x.find('check') != -1:
            result = getattr(achievChecks,x)(nick,host,message)
            if result:
                if len(results) == 0:
                    results = result
                else:
                    results = results + ' , ' + result
    if len(results) > 0:
        blurb = '~Congratulations %s you unlocked ' %nick
        if config.tumblr_tumbling:
            dontcare , url , atall = tumble.getLastPost('fuckyeahcutetranschicks')
            caption = '%s unlocked the following achievements : ' %nick + results
            tumbleUrl = tumble.makePost(config.tumblr_user,config.tumblr_password,config.tumblr_blog,config.tumblr_title,url,caption,caption)
            return blurb + results + ' - View your amazing achievements here http://%s' %tumbleUrl
        else:
            return blurb + results
    else:
        return None

def hook(nick, ident, host, message):
    db.execute("create table if not exists achiv(aid integer , host text , value integer)")
    if re.match('.achievements',message):
        result = achievChecks.listAchievs(host)
        if result == '':
            return 'You have no achievements %s , you loser' %nick
        else:
            return 'You have the following achievements : %s' %result
    else:                
        result = checkAchievs(nick , host, message)
        db.commit()
        return result
