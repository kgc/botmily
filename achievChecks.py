from __future__ import division
from __future__ import unicode_literals

import re

from botmily.db import db

KV_SHMLE = 1
KV_TRNY = 2
KV_HC_SB = 3
KV_COMPLETE = 4 

IMA_TRANNY = 5

def getAchiev(achievId , host):
    cur = db.execute("select * from achiv where host='%s' and aid=%i" %(host,achievId))
    result = cur.fetchall()
    if len(result) == 1:
        return result[0][2]
    elif len(result) > 1:
        print 'porblem'
        return -1
    elif len(result) == 0:
        return -1

def incrementAchiev(achievId , host):
    cur = db.execute("select * from achiv where host='%s' and aid=%i" %(host,achievId))
    result = cur.fetchall()
    if len(result) == 1:
        db.execute("update achiv set value=%i where host='%s' and aid=%i" %(result[0][2] + 1 , host , achievId))
        curVal =  result[0][2]
        return result[0][2] + 1
    elif len(result) > 1:
        print 'porblem'
        return 0
    elif len(result) == 0:
        db.execute("insert into achiv(aid, host , value) values(%i, '%s' , 1)" %(achievId,host))
        return 1

def checkKateV(nick , host , message):
    if getAchiev(KV_COMPLETE,host) != 1:
        if re.match('shemale' , message):
            incrementAchiev(KV_SHMLE,host)
        if re.match('tranny', message):
            incrementAchiev(KV_TRNY,host)
        if re.match('hard cocks on soft bodies', message):
            incrementAchiev(KV_HC_SB,host)
        s = getAchiev(KV_SHMLE,host)
        t = getAchiev(KV_TRNY,host)
        hc = getAchiev(KV_HC_SB,host)       
        if s >= 1 and t >= 1 and hc >= 1:
            incrementAchiev(KV_COMPLETE , host)
            return '~Congratulations , %s you unlocked the KateV achievment! You should check your privledge~' %nick
    return None

def checkImATranny(nick,host,message):
    if re.match('im a tranny' , message):
        result = incrementAchiev(1,host)
        if getAchiev(IMA_TRANNY , host) == 2:
            return '~Congratulations , %s you unlocked the tranny achievment!!~' %nick
    return None