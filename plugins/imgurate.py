import urllib2
import urllib
from xml.etree import ElementTree

def upload(message_data, bot):
	""" Rehosts a link onto imgur. 50 uploads per hour max. """
	r = urllib2.Request(url='http://api.imgur.com/2/upload.xml')
	r.add_data(urllib.urlencode({'key' : 'c65c4bc475794794df87407bc1e89789','image' : message_data}))
	try:
		response = urllib2.urlopen(r)
	except urllib2.URLError:
		return "Trouble uploading image."
	try:
		root = ElementTree.fromstring(response.read())
	except ElementTree.ParseError:
		return "Trouble uploading image."
	links = root.find('links')
	if links is None:
		return "Trouble uploading image."
	return links.find('original').text

def random(message_data, bot):
	""" Gets a Random image from imgur. """
	try:
		response = urllib2.urlopen('http://imgur.com/gallery/random.xml')
	except urllib2.URLError:
		return "Trouble getting image."
	try:
		root = ElementTree.fromstring(response.read())
	except ElementTree.ParseError:
		return "Trouble getting image."
	item = root.find('item')
	if item is None:
		return "Trouble getting image."
	hash = item.find('hash').text
	imageurl = 'http://imgur.com/' + hash
	return "Here's a random image: " + imageurl 
	

commands = {'imgur upload' : upload,'upload' : upload,'imgur random' : random,'random' : random}
triggers = []