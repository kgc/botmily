from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sqlite3

db = None

def connect():
    global db
    db = sqlite3.connect("botmily.db")