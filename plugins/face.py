from __future__ import division
from __future__ import unicode_literals
from urlparse import urlparse
import random
import re
import httplib, urllib , base64 , json 
import faceapi , imgur
from botmily.db import db
from botmily import config
from pprint import pprint
import faceSquares, imgur


regex = r'\(?\bhttp://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]'


def checkValidImage(url):
    lowerurl = url.lower()
    if lowerurl.endswith('.jpg') or lowerurl.endswith('.png') or lowerurl.endswith('.jpeg') or lowerurl.endswith('.gif'):
        try:
            urllib.urlopen(url)
        except IOError:
            return "URL Unreachable or something idk fix ur shit"
    else:
        return 'Not recognized image type , type .jpg , .png , .jpeg or .gif'    
    return None

def hook(nick, ident, host, message, bot, channel):    
    if re.match('.face help' , message):
        return 'Usage , .face <imgurl> OR .passmeter <imgurl> , to let it recognize your face.learn <your face img> '
    if re.match('.face', message) or re.match('.passmeter',message):
        imgurl = message.lstrip('.face ')
        imgurl = imgurl.lstrip('.passmeter ')
        invalid = checkValidImage(imgurl)
        if invalid:
            return invalid   
        result = faceapi.Detect(imgurl)
        result = faceapi.cleanTags(result)
        characteristics = faceapi.makeBlurb(result)
        if characteristics:
            img = faceSquares.drawTags(result['photos'][0]['tags'],imgurl)
            img.save('temp.png', 'PNG')
            postedUrl = imgur.postToImgur(str('temp.png'))
        result = faceapi.Recognize(imgurl)
        who = faceapi.getPeopleBlurb(result)
        if who and characteristics:
            return characteristics + who + ', what I saw %s' %postedUrl
        elif characteristics:
            return characteristics + ', what I saw %s' %postedUrl
        else:
            return "Couldn't find a face :("

    if re.match('.recognize',message):
        imgurl = message.lstrip('.recognize ')
        invalid = checkValidImage(imgurl)
        if invalid:
            return invalid   
        result = faceapi.Recognize(imgurl)
        return faceapi.getPeopleBlurb(result)

    if re.match('.learn',message):
        db.execute("create table if not exists face(nick integer , tid text)")
        imgurl = message.lstrip('.learn ')
        invalid = checkValidImage(imgurl)
        if invalid:
            return invalid   
        return faceapi.trainFace(imgurl,nick)

    if re.match('.remove',message):
        return faceapi.removeMe(nick)
    

    image_uri = re.search(regex, message, re.I)
    if image_uri is None:
        return None
    image_uri = image_uri.group(0)
    invalid = checkValidImage(image_uri)
    if invalid:
        return None
    result = faceapi.Recognize(image_uri)
    people = faceapi.getPeopleBlurb(result)
    if people:
        return people + ' ' + image_uri




