from __future__ import division
from __future__ import unicode_literals

import re

from botmily.db import db

KV_SHMLE = 1
KV_TRNY = 2
KV_HC_SB = 3
KV_COMPLETE = 4
KV_STRING = '~KateV Wannabe~'
IMA_TRANNY = 5
IMA_TRANNY_STRING = '~Transthusiast~' 
IMA_TRANNY_THRESH = 5
IM_GAY = 6
IM_GAY_THRESH = 5
IM_GAY_STRING = '~You Are Indeed Gay!~'
SAME = 7
SAME_THRESH = 5
SAME_STRING = "~Everybody's The Same!~"
DORA = 54
DORA_STRING = '~Literally Theodora IRL~'
IRL = 8
IRL_THRESH = 5
IRL_STRING = "~Reality Check~"
BUTT = 29
BUTT_THRESH = 5
BUTT_STRING = '~The Posterior Is Superior~'
BLIP_COMPLETE = 30
BLIP_CUTE = 31
BLIP_HOT = 32
BLIP_SHORT = 33
BLIP_STRING = '~Blippy Is Shorter Than You~'
GIRL = 34
GIRL_THRESH = 20
GIRL_STRING = "~I'm Not A Girl, Not Yet A Woman~" 
DICK = 35
DICK_THRESH = 20
DICK_STRING = "~KEEP SAYING DICK~" 
LOLIDK_COMPLETE = 36
LOLIDK_IDK = 37
LOLIDK_LOL = 38
LOLIDK_STRING = '~Ignorant But Laughing About It~'
CRUELTY = 39
CRUELTY_THRESH = 20
CRUELTY_STRING = "~Stop Fucking Laughing At People You Asshole!~" 
SAMANTHA = 40
SAMANTHA_THRESH = 10
SAMANTHA_STRING = "~Say My Name Bitch~" 
FML = 41
FML_THRESH = 10
FML_STRING = "~NO FUCK YOUR LIFE ASSHOLE~" 
FART = 42    
FART_THRESH = 5
FART_STRING = "~Farts Are Always Funny~" 
LINES = 43
LINES_THRESH = 1000
LINES_COMPLETE = 56
LINES_STRING = "~A Thousand Lines Of Bullshit, Hope You Are Happy!~" 
CREEP_COMPLETE = 44
CREEP_CREEP = 45
CREEP_WIERDO = 46
CREEP_HELL = 47
CREEP_BELONG = 48
CREEP_STRING = '~RADIOHEAD IS THE BEST BAND IN THE WORLD PROBABLY!!!~'
LINK = 49
LINK_THRESH = 10
LINK_STRING = "~I Hope All Those Links Are Funny!~" 
MAYHEM_COMPLETE = 50
MAYHEM_ROCKS = 51
MAYHEM_LIFTING = 52
MAYHEM_STRING = '~LIFT ROCKS EVRRDAY -- Mayhem 2012~'
TMT = 53
TMT_THRESH = 5
TMT_STRING = "~Stop Reading That Fucking Thread~" 

#next achiev must use 57 or higher

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
    
def listAchievs(host):
    achievs = ''
    if getAchiev(KV_COMPLETE,host) >= 1:
        achievs = achievs + KV_STRING
    if getAchiev(IMA_TRANNY,host) >= IMA_TRANNY_THRESH:
        achievs = achievs + ' ' + IMA_TRANNY_STRING
    if getAchiev(IM_GAY,host) >= IM_GAY_THRESH:
        achievs = achievs + ' ' + IM_GAY_STRING
    if getAchiev(SAME,host) >= SAME_THRESH:
        achievs = achievs + ' ' + SAME_STRING
    if getAchiev(DORA,host) >= 1:
        achievs = achievs + ' ' + DORA_STRING
    if getAchiev(IRL,host) >= IRL_THRESH:
        achievs = achievs + ' ' + IRL_STRING
    if getAchiev(BUTT,host) >= BUTT_THRESH:
        achievs = achievs + ' ' + BUTT_STRING
    if getAchiev(BLIP_COMPLETE,host) >= 1:
        achievs = achievs + ' ' + BLIP_STRING
    if getAchiev(GIRL,host) >= GIRL_THRESH:
        achievs = achievs + ' ' + GIRL_STRING
    if getAchiev(DICK,host) >= DICK_THRESH:
        achievs = achievs + ' ' + DICK_STRING
    if getAchiev(LOLIDK_COMPLETE,host) >= 1:
        achievs = achievs + ' ' + LOLIDK_STRING
    if getAchiev(CRUELTY,host) >= CRUELTY_THRESH:
        achievs = achievs + ' ' + CRUELTY_STRING
    if getAchiev(SAMANTHA,host) >= SAMANTHA_THRESH:
        achievs = achievs + ' ' + SAMANTHA_STRING
    if getAchiev(FML,host) >= FML_THRESH:
        achievs = achievs + ' ' + FML_STRING
    if getAchiev(FART,host) >= FART_THRESH:
        achievs = achievs + ' ' + FART_STRING
    if getAchiev(LINES_COMPLETE,host) >= 1:
        achievs = achievs + ' ' + LINES_STRING
    if getAchiev(CREEP_COMPLETE,host) >= 1:
        achievs = achievs + ' ' + CREEP_STRING
    if getAchiev(LINK,host) >= LINK_THRESH:
        achievs = achievs + ' ' + LINK_STRING
    if getAchiev(MAYHEM_COMPLETE,host) >= 1:
        achievs = achievs + ' ' + MAYHEM_STRING
    if getAchiev(TMT,host) >= TMT_THRESH:
        achievs = achievs + ' ' + TMT_STRING
    return achievs

def checkKateV(nick , host , message):
    if getAchiev(KV_COMPLETE,host) < 1:
        if re.search('shemale' , message):
            incrementAchiev(KV_SHMLE,host)
        if re.search('tranny', message):
            incrementAchiev(KV_TRNY,host)
        if re.search('hard cocks on soft bodies', message):
            incrementAchiev(KV_HC_SB,host)
        s = getAchiev(KV_SHMLE,host)
        t = getAchiev(KV_TRNY,host)
        hc = getAchiev(KV_HC_SB,host)       
        if s >= 1 and t >= 1 and hc >= 1:
            incrementAchiev(KV_COMPLETE , host)
            return KV_STRING
    return None

def checkImATranny(nick,host,message):
    if re.search('im a tranny' , message):
        result = incrementAchiev(IMA_TRANNY,host)
        if getAchiev(IMA_TRANNY , host) == IMA_TRANNY_THRESH:
            return IMA_TRANNY_STRING
    return None


def checkImGay(nick,host,message):
    if re.search('im gay' , message):
        result = incrementAchiev(IM_GAY,host)
        if getAchiev(IM_GAY , host) == IM_GAY_THRESH:
            return IM_GAY_STRING
    return None


def checkSame(nick,host,message):
    if re.search('same' , message):
        result = incrementAchiev(SAME,host)
        if getAchiev(SAME , host) == SAME_THRESH:
            return SAME_STRING
    return None

def checkTheodora(nick,host,message):
    if getAchiev(SAME , host) > 15 and getAchiev(IM_GAY,host) > 15:
        if getAchiev(DORA_COMPLETE,host) < 1:       
            incrementAchiev(DORA_COMPLETE , host)
            return DORA_STRING
    return None


def checkIrl(nick,host,message):
    if re.search('irl' , message):
        result = incrementAchiev(IRL,host)
        if getAchiev(IRL , host) == IRL_THRESH:
            return 
    return None

def checkButts(nick,host,message):
    if re.search('butt',message):
        result = incrementAchiev(BUTT,host)
        if getAchiev(BUTT,host) == BUTT_THRESH:
            return "The Posterior Is Superior!" 

def checkBlippy(nick , host , message):
    if getAchiev(BLIP_COMPLETE,host) < 1:
        if re.search('cute' , message):
            incrementAchiev(BLIP_CUTE,host)
        if re.search('hot', message):
            incrementAchiev(BLIP_HOT,host)
        if re.search('short', message) or re.search('shortest',message):
            incrementAchiev(BLIP_SHORT,host)
        s = getAchiev(BLIP_CUTE,host)
        t = getAchiev(BLIP_HOT,host)
        hc = getAchiev(BLIP_SHORT,host)       
        if s >= 2 and t >= 2 and hc >= 2:
            incrementAchiev(BLIP_COMPLETE , host)
            return BLIP_STRING
    return None


def checkGirl(nick,host,message):
    if re.search('girl',message):
        result = incrementAchiev(GIRL,host)
        if getAchiev(GIRL,host) == GIRL_THRESH:
            return GIRL_STRING

def checkDick(nick,host,message):
    if re.search('dick',message):
        result = incrementAchiev(DICK,host)
        if getAchiev(DICK,host) == DICK_THRESH:
            return DICK_STRING


def checkLOLIDK(nick , host , message):
    if getAchiev(LOLIDK_COMPLETE,host)  < 1:
        if re.search('idk' , message):
            incrementAchiev(LOLIDK_IDK,host)
        if re.search('lol', message):
            incrementAchiev(LOLIDK_LOL,host)
        t = getAchiev(LOLIDK_LOL,host)
        hc = getAchiev(LOLIDK_IDK,host)       
        if hc >= 4 and t >= 4:
            incrementAchiev(LOLIDK_COMPLETE , host)
            return LOLIDK_STRING
    return None


def checkCruelty(nick,host,message):
    if re.search('lol @',message):
        result = incrementAchiev(CRUELTY,host)
        if getAchiev(CRUELTY,host) == CRUELTY_THRESH:
            return CRUELTY_STRING


def checkSamantha(nick,host,message):
    if re.search('samantha',message):
        result = incrementAchiev(SAMANTHA,host)
        if getAchiev(SAMANTHA,host) == SAMANTHA_THRESH:
            return SAMANTHA_STRING

       
def checkFML(nick,host,message):
    if re.search('.fml',message):
        result = incrementAchiev(FML,host)
        if getAchiev(FML,host) == FML_THRESH:
            return FML_STRING
    
def checkFart(nick,host,message):
    if re.search('fart',message):
        result = incrementAchiev(FART,host)
        if getAchiev(FART,host) == FART_THRESH:
            return FART_STRING

def checkLines(nick,host,message):
    incrementAchiev(LINES,host)
    if getAchiev(LINES,host) == 1000:
        incrementAchiev(LINES_COMPLETE,host)
        return LINES_STRING


def checkCreep(nick,host,message):
    if getAchiev(CREEP_COMPLETE,host) < 1:
        if re.search('im a creep' , message):
            incrementAchiev(CREEP_CREEP,host)
        if re.search('im a wierdo', message):
            incrementAchiev(CREEP_WIERDO,host)
        if re.search('what the hell am i doing here', message):
            incrementAchiev(CREEP_HELL,host)
        if re.search('i dont belong here', message):
            incrementAchiev(CREEP_BELONG,host)
        c = getAchiev(CREEP_CREEP,host)
        w = getAchiev(CREEP_WIERDO,host)    
        h = getAchiev(CREEP_HELL,host)
        b = getAchiev(CREEP_BELONG,host)   
        if c >= 1 and w >= 1 and h >=1 and b >= 1:
            incrementAchiev(CREEP_COMPLETE , host)
            return CREEP_STRING
    return None


def checkLink(nick,host,message):
    if re.search('http://',message , re.IGNORECASE):
        result = incrementAchiev(LINK,host)
        if getAchiev(LINK,host) == LINK_THRESH:
            return LINK_STRING


def checkMayhem(nick , host , message):
    if getAchiev(MAYHEM_COMPLETE,host) < 1:
        if re.search('rocks' , message , re.IGNORECASE):
            incrementAchiev(MAYHEM_ROCKS,host)
        if re.search('lifting', message , re.IGNORECASE) or re.search('lift',message,re.IGNORECASE):
            incrementAchiev(MAYHEM_LIFTING,host)
        t = getAchiev(MAYHEM_ROCKS,host)
        hc = getAchiev(MAYHEM_LIFTING,host)       
        if hc >= 2 and t >= 2:
            incrementAchiev(MAYHEM_COMPLETE , host)
            return MAYHEM_STRING
    return None


def checkTMT(nick,host,message):
    if re.search('threadid=3447636',message , re.IGNORECASE):
        result = incrementAchiev(TMT,host)
        if getAchiev(TMT,host) == TMT_THRESH:
            return TMT_STRING
