# -*- coding: latin-1 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen
from xml.etree import ElementTree

def hook(message):
    if re.match('.wea', message) is None:
        return None
    if len(message) < 6:
        return 'Type in a location ¬_¬'.encode('latin-1')
    result = urlopen('http://www.google.com/ig/api?weather=' + message[5:])
    root = ElementTree.fromstring(result.read())
    weather = root.find('weather')
    forecast_information = weather.find('forecast_information')
    current_conditions = weather.find('current_conditions')
    forecast_conditions = weather.find('forecast_conditions')
    string = forecast_information.find('city').get('data') + ': '
    string = string + current_conditions.find('condition').get('data') + ', '
    string = string + current_conditions.find('temp_f').get('data') + 'F/'
    string = string + current_conditions.find('temp_c').get('data') + 'C (H:'
    string = string + forecast_conditions.find('high').get('data') + 'F, L:'
    string = string + forecast_conditions.find('low').get('data') + 'F), '
    string = string + current_conditions.find('humidity').get('data') + ', '
    string = string + current_conditions.find('wind_condition').get('data') + '.'
    return string
