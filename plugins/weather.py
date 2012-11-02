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
        result = urllib2.urlopen('http://api.wunderground.com/api/91ef6bb1dc828118/conditions/q/' + loc + '.xml')
    except urllib2.URLError:
        return "Error getting weather data"
    try:
        root = ElementTree.fromstring(result.read())
    except ElementTree.ParseError:
        return "Error getting weather data"
    current_observation = weather.find('forecast_information')
    if current_observation is None:
        return "Error getting weather data"
    display_location = weather.find('display_location')
    string = display_location.find('full').get() + ': '
    string = string + current_observation.find('weather').get() + ', '
    string = string + current_observation.find('temperature_string').get() + ', '
    string = string + current_observation.find('relative_humidity').get() + ', Wind is blowing '
    string = string + current_observation.find('wind_string').get().replace('F','f', 1) + '.'
    return string

commands = {"weather": weather}
triggers = []

