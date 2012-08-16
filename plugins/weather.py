# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import urllib2
from xml.etree import ElementTree

from botmily.db import db

def weather(message_data, bot):
    db.execute("create table if not exists weather(nick primary key, loc)")
    loc = message_data["parsed"]
    if loc == "":
        row = db.execute("select loc from weather where nick=:nick", {"nick": message_data["nick"]}).fetchone()
        if not row:
            return 'Type in a location ¬_¬'
        loc = row[0]
    else:
        db.execute("insert or replace into weather(nick, loc) values (:nick, :loc)", {"nick": message_data["nick"], "loc": loc})
        db.commit()
    try:
        result = urllib2.urlopen('http://www.google.com/ig/api?weather=' + loc)
    except urllib2.URLError:
        return "Error getting weather data"
    root = ElementTree.fromstring(result.read())
    weather = root.find('weather')
    forecast_information = weather.find('forecast_information')
    if forecast_information is None:
        return "Error getting weather data"
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

commands = {"weather": weather}
triggers = []

