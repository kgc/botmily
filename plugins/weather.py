# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib2 import urlopen
from xml.etree import ElementTree

from botmily.db import db

def hook(nick, ident, host, message):
    if re.match('.wea', message) is None:
        return None

    db.execute("create table if not exists weather(nick primary key, loc)")
    loc = message[5:]
    if len(message) < 6:
        row = db.execute("select loc from weather where nick=:nick", {"nick": nick}).fetchone()
        if not row:
            return 'Type in a location ¬_¬'.encode('latin-1')
        loc = row[0]
    else:
        db.execute("insert or replace into weather(nick, loc) values (:nick, :loc)", {"nick": nick, "loc": loc})
        db.commit()
    result = urlopen('http://www.google.com/ig/api?weather=' + loc)
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
