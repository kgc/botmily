'''Searches wikipedia and returns first sentence of article
Scaevolus 2009'''


from xml.dom.minidom import parseString
import httplib, urllib 

USER_AGENT = 'botmily python irc bot'
def extract(item):
    description = item.getElementsByTagName('Description')[0].childNodes[0].nodeValue
    title = item.getElementsByTagName('Text')[0].childNodes[0].nodeValue
    url = item.getElementsByTagName('Url')[0].childNodes[0].nodeValue
    return title.strip(),description.strip(),url

def wiki(message_data, bot):
    '''.w/.wiki <phrase> -- gets first sentence of wikipedia ''' \
    '''article on <phrase>'''
    httpcnx = httplib.HTTPConnection('en.wikipedia.org' , strict = True)    
    url = "/w/api.php/?action=opensearch&format=xml&" + urllib.urlencode( {'search':message_data['parsed']} )
    headers = {'User-Agent':USER_AGENT}
    httpcnx.request('POST' , url , None ,headers)
    response = httpcnx.getresponse() 
    xml = parseString(response.read())
    items = xml.getElementsByTagName('Item')
    if len(items) > 0:
        title,description,url = extract(items[0])
        if 'may refer to' in description:
            title,description,url = extract(items[1])
        if len(description) > 300:
            description = description[:300] + '...'
        ret = '%s -- %s' %(description, urllib.quote(url, ':/'))
        return ret
    else:
        return 'No results'




commands = {"wiki": wiki}
triggers = []