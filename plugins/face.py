from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from urlparse import urlparse
import random
import re
import httplib, urllib , base64 , json 
def hook(nick, ident, host, message):
    if re.match('.face', message) or re.match('.passmeter',message):
        imgurl = message.lstrip('.face ')
        imgurl = imgurl.lstrip('.passmeter ')
        lowerurl = imgurl.lower()
        if lowerurl.endswith('.jpg') or lowerurl.endswith('.png') or lowerurl.endswith('.jpeg') or lowerurl.endswith('.gif'):
            try:
                urllib.urlopen(imgurl)
            except IOError:
                return "URL Unreachable or something idk fix ur shit"
        else:
            return 'Not recognized image type , type .jpg , .png , .jpeg or .gif'

        o = urlparse(imgurl)
        httpcnx = httplib.HTTPSConnection('api.face.com' , strict = True)    
        params = {'api_key' : '2fffccb658f4e2b092bc2360e3a6ea27' , 'api_secret' : 'ecf5262853523b43625a5c384977e259' , 'urls' : imgurl ,'detector' : 'Aggressive'}
        url = "/faces/detect.json" 
        url = url + "?" + urllib.urlencode( params )
        httpcnx.request('GET' , url )
        response = httpcnx.getresponse()           
        x = json.loads(response.read())
        if x['photos'][0].has_key('tags'):
            if x['photos'][0]['tags'][0]['attributes'].has_key('mood') and x['photos'][0]['tags'][0]['attributes'].has_key('gender') :            
                genderVal =  x['photos'][0]['tags'][0]['attributes']['gender']['value']
                moodVal = x['photos'][0]['tags'][0]['attributes']['mood']['value']
                moodConfidence = x['photos'][0]['tags'][0]['attributes']['mood']['confidence']
                genderConfidence =  x['photos'][0]['tags'][0]['attributes']['gender']['confidence']
                return 'Person is %s  with %s%% confidence, current mood %s with %s%% confidence ' %(genderVal , genderConfidence , moodVal , moodConfidence)

            elif x['photos'][0]['tags'][0]['attributes'].has_key('gender'):            
                genderVal =  x['photos'][0]['tags'][0]['attributes']['gender']['value']
                genderConfidence =  x['photos'][0]['tags'][0]['attributes']['gender']['confidence']
                return 'Person is %s  with %s%% confidence' %(genderVal , genderConfidence)
            else:
                return "Couldn't find a face or something , mebbe too ugly?"
        else:
            return "Couldn't find a face or something , mebbe too ugly?"

    return None




