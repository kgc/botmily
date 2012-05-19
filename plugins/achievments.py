from __future__ import division
from __future__ import unicode_literals

import re

from botmily.db import db
import achievChecks

def checkAchievs(nick , host , message):
    results = ''
    for x in dir(achievChecks):
        if x.find('check') != -1:
            result = getattr(achievChecks,x)(nick,host,message)
            if result:
                results = results + ' ' + result
    return results
   
def hook(nick, ident, host, message):
    db.execute("create table if not exists achiv(aid integer , host text , value integer)")
    result = checkAchievs(nick , host, message)
    db.commit()
    return result
