import tumblr
import urllib2 , urllib
from PIL import Image
from cStringIO import StringIO
from makeMacro import overlayAchieve
import pycurl
def postToImgur(filename):    
    store = StringIO()
    c = pycurl.Curl()
    values = [
              ("key", "a95e5a7d90d1f821714e449bb47e1051"),
              ("image", (c.FORM_FILE, filename))]
    c.setopt(c.URL, "http://api.imgur.com/2/upload.xml")
    c.setopt(c.HTTPPOST, values)
    c.setopt(c.WRITEFUNCTION,store.write)
    c.perform()
    c.close()

    retval = store.getvalue()
    originalindex = retval.rfind('<original>')
    endindex = retval.find('</original>')
    urlneeded = retval[originalindex+10:endindex]
    return urlneeded

def makePost(user,password,blog,title,imgUrl,caption,tumblrCaption):
    filename = overlayAchieve(caption,imgUrl)
    url = 'http://www.tumblr.com/api/write'
    imageurl = postToImgur('./%s'%filename)
    vals = {
                'email': user,
                'password': password,
                'type': 'photo',
                'source': imageurl,
                'caption':tumblrCaption,
                'group':blog
            }
    data = urllib.urlencode(vals)
    req = urllib2.Request(url,data)
    try:
            response = urllib2.urlopen(req)
            postId = response.read()
            postUrl = blog + '/post/%s' %postId
            return postUrl
    except urllib2.URLError, e:
            print e.code
            print e.read()
            return None
        
def getLastPost(blogName):        
    blogApi= tumblr.Api(blogName)
    blog = blogApi.read()
    lastpost = blog.next()
    return unicode(lastpost['url-with-slug']) , unicode(lastpost['photo-url-1280']) , unicode(lastpost['url-with-slug'])