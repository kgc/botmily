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

def face(message_data, bot):
    imgurl = message_data["parsed"]
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

commands = {"face": face, "passmeter": face}
triggers = []

