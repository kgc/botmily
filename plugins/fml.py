from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen
from xml.etree import ElementTree

from BeautifulSoup import BeautifulSoup

def hook(nick, ident, host, message):
    if re.match('.fml', message) is None:
        return None
    response = urlopen('http://m.fmylife.com/random')
    html = response.read().decode('utf-8').replace("&mdash;", "").replace("&rarr;", "").replace("&copy;", "")
    root = ElementTree.fromstring(BeautifulSoup(html).prettify())
    match = root.findall('{http://www.w3.org/1999/xhtml}body/{http://www.w3.org/1999/xhtml}ul/{http://www.w3.org/1999/xhtml}li/{http://www.w3.org/1999/xhtml}p')[1]
    return match.text.strip()
