
from __future__ import unicode_literals
import httplib, urllib , base64 , json 
from botmily.db import db
import pprint

def Detect(imageUrl):
    httpcnx = httplib.HTTPSConnection('api.face.com' , strict = True)    
    params = {'api_key' : '2fffccb658f4e2b092bc2360e3a6ea27' , 'api_secret' : 'ecf5262853523b43625a5c384977e259' , 'urls' : imageUrl ,'detector' : 'Aggressive' ,'attributes' : 'all'}
    url = "/faces/detect.json" 
    url = url + "?" + urllib.urlencode( params )
    httpcnx.request('GET' , url )
    response = httpcnx.getresponse()           
    return json.loads(response.read())

def Recognize(imageUrl):
    httpcnx = httplib.HTTPSConnection('api.face.com' , strict = True)    
    params = {'api_key' : '2fffccb658f4e2b092bc2360e3a6ea27' , 'api_secret' : 'ecf5262853523b43625a5c384977e259' , 'urls' : imageUrl ,'uids' : 'all@shughes.uk' ,'detector' : 'Aggressive'}
    url = "/faces/recognize.json" 
    url = url + "?" + urllib.urlencode( params )
    httpcnx.request('GET' , url )
    response = httpcnx.getresponse()           
    return json.loads(response.read())

def SaveTag(tid,userid):
    httpcnx = httplib.HTTPSConnection('api.face.com' , strict = True)    
    params = {'api_key' : '2fffccb658f4e2b092bc2360e3a6ea27' , 'api_secret' : 'ecf5262853523b43625a5c384977e259' , 'tids' : tid ,'uid' : userid + '@shughes.uk' }
    url = "/tags/save.json" 
    url = url + "?" + urllib.urlencode( params )
    httpcnx.request('GET' , url )
    response = httpcnx.getresponse()           
    return json.loads(response.read())

def RemoveTag(tid):
    httpcnx = httplib.HTTPSConnection('api.face.com' , strict = True)    
    params = {'api_key' : '2fffccb658f4e2b092bc2360e3a6ea27' , 'api_secret' : 'ecf5262853523b43625a5c384977e259' , 'tids' : tid  }
    url = "/tags/remove.json" 
    url = url + "?" + urllib.urlencode( params )
    httpcnx.request('GET' , url )
    response = httpcnx.getresponse()           
    return json.loads(response.read())

def Train(userid):
    httpcnx = httplib.HTTPSConnection('api.face.com' , strict = True)    
    params = {'api_key' : '2fffccb658f4e2b092bc2360e3a6ea27' , 'api_secret' : 'ecf5262853523b43625a5c384977e259' , 'uids' : userid + '@shughes.uk' }
    url = "/faces/train.json" 
    url = url + "?" + urllib.urlencode( params )
    httpcnx.request('GET' , url )
    response = httpcnx.getresponse()           
    return json.loads(response.read())

def makeBlurb(face):
    blurb = ''
    try:
        if len(face['photos']) == 1:
            photo = face['photos'][0]
            if photo.has_key('tags'):
                facecount = 0
                for tag in photo['tags']:
                    if len(tag['attributes'].keys()) > 1:
                        facecount += 1
                if facecount > 1:
                    blurb = '%s faces in this photo ,' %facecount
                    for tag in photo['tags']:
                        if len(tag['attributes'].keys()) > 1:
                            blurb = blurb +' Face %i:  ' %faceNum +  getTagBlurb(tag) 
                            faceNum += 1
                elif facecount == 1:                
                    blurb = 'One face in this photo ,' + getTagBlurb(tag)
                else:
                    return None
                faceNum = 1
                
                return blurb
    except Exception , e:
        print e
        print '\nFace Json :'
        print face
    return None

def getTagBlurb(tag):
    stringDict = {'gender' : '' , 'age' : '' , 'face' : '','glasses':'' , 'smiling':'' , 'lips':'' , 'mood': ''}
    attributes = tag['attributes']    
    for attribute in attributes:
        if attribute == 'gender':
            stringDict['gender'] = " \u0002Gender\u000f %s (%s%%)" %(attributes[attribute]['value'],attributes[attribute]['confidence'])

        if attribute == 'age_est':
            stringDict['age'] = " \u0002Age\u000f: %s (%s%%)" %(attributes[attribute]['value'],attributes[attribute]['confidence'])

        if attribute == 'mood':
            stringDict['mood'] =  " \u0002Mood\u000f: %s (%s%%) "%(attributes[attribute]['value'],attributes[attribute]['confidence'])
    blurb = stringDict['gender'] + stringDict['age'] + stringDict['mood'] 
    return blurb

def getPeopleBlurb(tags):
    blurb = ''
    users =[]
    try:
        if len(tags['photos']) == 1:
            photo = tags['photos'][0]
            if photo.has_key('tags'):
                for tag in photo['tags']:
                    if len(tag['uids']) > 0:
                        users.append(tag['uids'][0]['uid'].rstrip('@shughes.uk'))
        if len(users) > 0:
            for user in users:
                blurb = blurb +  '%s ,' %user
            return blurb + ' could be in this photo'
        else:
            return None
    except Exception , e:
        print e
        print '\nFace Json :'
        print tags
    return None

def getTag(face):
    if len(face['photos']) == 1:
            photo = face['photos'][0]
            if photo.has_key('tags'):
                if len(photo['tags']) == 1:
                    return photo['tags'][0]
    return None

def trainFace(imageUrl,nick):
    detectResult = Detect(imageUrl)
    tag = getTag(detectResult)
    if tag:
        tid = tag['tid']
        savedTIDS = getSavedTIDS(nick)
        for s_tid in savedTIDS:
            tid = tid + ',' + s_tid
        x = SaveTag(tid,nick)
        saved_tags = x['saved_tags']
        for tag in saved_tags:
            saveTID(nick,tag['tid'])
        result = Train(nick)
        if result.has_key('updated'):
            return "I now have %s picture's of %s maybe ill get good at recognizing them" %(result['updated'][0]['training_set_size'], nick)
        elif result.has_key('unchanged'):
            return 'I think I already had that picture , nothing changed'
    else:
        return "Multiple faces or I coulndt find any at all"

def removeMe(nick):
    tids = getSavedTIDS(nick)
    tid = ''
    for result in tids:
        tid += result
    RemoveTag(tid)
    db.execute("delete from face where nick='%s'" %nick)
    db.commit()
    return 'Done'



def getSavedTIDS(nick):
    cur = db.execute("select * from face where nick='%s'" %nick)
    result = cur.fetchall()
    results = []
    if len(result) > 0:
        for row in result:
            results.append(row[1])
        return results
    elif len(result) == 0:
        return []

def saveTID(nick , tid):
    cur = db.execute("select * from face where nick='%s' and tid='%s'" %(nick,tid))
    result = cur.fetchall()
    if len(result) == 1:
        print 'TID already exists for nick'
    elif len(result) > 1:
        print 'porblem'
    elif len(result) == 0:
        print 'Saving Tag %s' %tid
        db.execute("insert into face(nick, tid) values('%s', '%s')" %(nick,tid))
    db.commit()