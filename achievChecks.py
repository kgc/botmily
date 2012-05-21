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
            return 'KateV Wannabe'
    return None

def checkImATranny(nick,host,message):
    if re.match('im a tranny' , message):
        result = incrementAchiev(IMA_TRANNY,host)
        if getAchiev(IMA_TRANNY , host) == 2:
            return 'Transthusiast' 
    return None

IM_GAY = 6
def checkImGay(nick,host,message):
    if re.match('im gay' , message):
        result = incrementAchiev(IM_GAY,host)
        if getAchiev(IM_GAY , host) == 20:
            return 'You Are Indeed Gay!'
    return None

SAME = 7
def checkSame(nick,host,message):
    if re.match('same' , message):
        result = incrementAchiev(SAME,host)
        if getAchiev(SAME , host) == 10:
            return "Everybody's The Same!"
    return None

def checkTheodora(nick,host,message):
        if getAchiev(SAME , host) == 15 && getAchiev(IM_GAY,host) == 15:
            return 'Literally Theodora IRL'
    return None

IRL = 8
def checkIrl(nick,host,message):
    if re.match('irl' , message):
        result = incrementAchiev(IRL,host)
        if getAchiev(IRL , host) == 10:
            return "Reality Check"
    return None

def checkButts(nick,host,message):
    if re.match('butt',message):
        result = incrementAchiev(BUTT,host)
        if getAchiev(BUTT,host) == 10:
            return "The Posterior Is Superior!" 

BLIP_COMPLETE = 9
BLIP_CUTE = 10
BLIP_HOT = 11
BLIP_SHORT = 12
def checkBlippy(nick , host , message):
    if getAchiev(BLIP_COMPLETE,host) != 1:
        if re.match('cute' , message):
            incrementAchiev(BLIP_CUTE,host)
        if re.match('hot', message):
            incrementAchiev(BLIP_HOT,host)
        if re.match('short', message) or re.match('shortest',message):
            incrementAchiev(BLIP_SHORT,host)
        s = getAchiev(BLIP_CUTE,host)
        t = getAchiev(BLIP_HOT,host)
        hc = getAchiev(BLIP_SHORT,host)       
        if s >= 2 and t >= 2 and hc >= 2:
            incrementAchiev(BLIP_COMPLETE , host)
            return 'Blippy Is Shorter Than You'
    return None

GIRL = 13
def checkGirl(nick,host,message):
    if re.match('girl',message):
        result = incrementAchiev(GIRL,host)
        if getAchiev(GIRL,host) == 20:
            return "I'm Not A Girl, Not Yet A Woman" 
DICK = 14
def checkDick(nick,host,message):
    if re.match('dick',message):
        result = incrementAchiev(DICK,host)
        if getAchiev(DICK,host) == 10:
            return "KEEP SAYING DICK" 

LOLIDK_COMPLETE =15
LOLIDK_IDK = 16
LOLIDK_LOL = 17
def checkLOLIDK(nick , host , message):
    if getAchiev(LOLIDK_COMPLETE,host) != 1:
        if re.match('idk' , message):
            incrementAchiev(LOLIDK_IDK,host)
        if re.match('lol', message):
            incrementAchiev(LOLIDK_LOL,host)
        t = getAchiev(LOLIDK_LOL,host)
        hc = getAchiev(LOLIDK_IDK,host)       
        if s >= 4 and t >= 4:
            incrementAchiev(BLIP_COMPLETE , host)
            return 'Ignorant But Laughing About It'
    return None

CRUELTY = 14
def checkCruelty(nick,host,message):
    if re.match('lol @',message):
        result = incrementAchiev(CRUELTY,host)
        if getAchiev(CRUELTY,host) == 5:
            return "Stop Fucking Laughing At People You Asshole!" 

SAMANTHA = 15
def checkSamantha(nick,host,message):
    if re.match('samantha',message):
        result = incrementAchiev(SAMANTHA,host)
        if getAchiev(SAMANTHA,host) == 5:
            return "Say My Name Bitch" 

FML = 16         
def checkFML(nick,host,message):
    if re.match('.fml',message):
        result = incrementAchiev(FML,host)
        if getAchiev(FML,host) == 8:
            return "NO FUCK YOUR LIFE ASSHOLE" 
FART = 17        
def checkFML(nick,host,message):
    if re.match('fart',message):
        result = incrementAchiev(FART,host)
        if getAchiev(FART,host) == 5:
            return "Farts Are Always Funny" 
LINK = 18
def checkFML(nick,host,message):
    incrementAchiev(LINK,host)
        if getAchiev(LINK,host) == 1000:
            return "A Thousand Lines Of Bullshit, Hope You Are Happy!" 

CREEP_COMPLETE = 19
CREEP_CREEP = 20
CREEP_WIERDO = 21
CREEP_HELL = 22
CREEP_BELONG = 23
def checkCreep(nick,host,message):
    if getAchiev(CREEP_COMPLETE,host) != 1:
        if re.match('im a creep' , message):
            incrementAchiev(CREEP_CREEP,host)
        if re.match('im a wierdo', message):
            incrementAchiev(CREEP_WIERDO,host)
        if re.match('what the hell am i doing here', message):
            incrementAchiev(CREEP_HELL,host)
        if re.match('i dont belong here', message):
            incrementAchiev(CREEP_BELONG,host)
        c = getAchiev(CREEP_CREEP,host)
        w = getAchiev(CREEP_WIERDO,host)    
        h = getAchiev(CREEP_HELL,host)
        b = getAchiev(CREEP_BELONG,host)   
        if c >= 1 and w >= 1 and h >=1 and b >= 1:
            incrementAchiev(CREEP_COMPLETE , host)
            return 'RADIOHEAD IS THE BEST BAND IN THE WORLD PROBABLY!!!'
    return None