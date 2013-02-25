from StringIO import StringIO
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
    try:
        c.perform()
    except pycurl.error:
        return "Try again fucko"
    c.close()
    retval = store.getvalue()
    originalindex = retval.rfind('<original>')
    endindex = retval.find('</original>')
    url = retval[originalindex+10:endindex]
    return url
