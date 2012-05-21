from __future__ import division
from __future__ import unicode_literals

import re

from botmily.db import db
import achievChecks

def checkAchievs(nick , host , message):
    results = None
    for x in dir(achievChecks):
        if x.find('check') != -1:
            result = getattr(achievChecks,x)(nick,host,message)
            if result:
                if len(results) == 0:
                    results = result
                else:
                    results = results + ' , ' + result
    if results:
        blurb = '~Congratulations %s you unlocked ' %nick
        return blurb + results + '~'
    else:
        return None

def hook(nick, ident, host, message):
    db.execute("create table if not exists achiv(aid integer , host text , value integer)")
    result = checkAchievs(nick , host, message)
    db.commit()
    return result
