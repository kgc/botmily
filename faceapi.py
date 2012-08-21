
from __future__ import unicode_literals
import httplib, urllib , base64 , json 
from botmily.db import db
import pprint

MASHAPE_AUTH = {'X-Mashape-Authorization': 'dWNwZDBxdnF1bjhjdnlveWdtZnNtdTBpdXhodWFrOmNlOGZiMGVlM2JkZTAzMTk0YmI2ZWNhZDBjNzMwOTFhYzQ2NzUyMTI='}

def Detect(imageUrl):
    httpcnx = httplib.HTTPSConnection('lambda-face-detection-and-recognition.p.mashape.com' , strict = True)    
    params = {'images':imageUrl}
    url = "/detect" 
    url = url + "?" + urllib.urlencode( params )
    httpcnx.request('GET' , url , None , MASHAPE_AUTH)
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
                    if len(tag['attributes'][0].keys()) > 1:
                        facecount += 1
                if facecount > 1:
                    blurb = '%s faces in this photo, ' %facecount
                    faceNum = 1
                    for tag in photo['tags']:
                        if len(tag['attributes'][0].keys()) > 1:
                            blurb = blurb +' Face %i: ' %faceNum +  getTagBlurb(tag) 
                            faceNum += 1
                elif facecount == 1:
                    blurb = 'One face in this photo, ' + getTagBlurb(tag)
                else:
                    return None
                
                return blurb
    except Exception , e:
        print e
        print '\nFace Json :'
        print face
    return None
    
def cleanTags(tags):
    tids = {}
    toPurge = []
    try:
        if len(tags['photos']) == 1:
            photo = tags['photos'][0]
            if photo.has_key('tags'):
                for tag in photo['tags']:
                    if tids.has_key(tag['tid']):
                        toPurge.append(tag)
                    elif len(tag['attributes'][0].keys()) < 2:
                        toPurge.append(tag)
                    else:
                        tids[tag['tid']] = True

    except Exception , e:
        print e
        print '\nFace Json :'
        print tags

    for tag in toPurge:
        tags['photos'][0]['tags'].remove(tag)
    return tags

def getTagBlurb(tag):
    stringDict = {'gender' : '' , 'age' : '' , 'face' : '','glasses':'' , 'smiling':'' , 'lips':'' , 'mood': ''}
    attributes = tag['attributes']   
    for attribute in attributes:
        if attribute.has_key('gender'):
            stringDict['gender'] = "\u0002%s\u000f(%s%%) " %(attribute['gender'],attribute['confidence'])

    blurb = stringDict['gender'] + stringDict['age'] + stringDict['mood'] 
    return blurb



def getTag(face):
    if len(face['photos']) == 1:
            photo = face['photos'][0]
            if photo.has_key('tags'):
                if len(photo['tags']) == 1:
                    return photo['tags'][0]
    return None
