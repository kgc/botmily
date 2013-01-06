# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import time

from botmily.db import db

def quote(message_data, bot):
    db.execute("create table if not exists quote(sender text, quote text, time integer)")
    if message_data["parsed"][:4] == "add ":
        db.execute("insert into quote(sender, quote, time) values (:sender, :quote, :time)", {"sender": message_data["nick"], "quote": message_data["parsed"][4:], "time": int(time.time())})
        db.commit()
        return "Quote added."
    elif message_data["parsed"][:7] == "search ":
        quotes = db.execute("select sender, quote, time from quote where quote like :quote", {"quote": "%" + message_data["parsed"][7:] + "%"}).fetchall()
        if len(quotes) == 0:
            return "Nothing found."
        row = random.choice(quotes)
        return "Found " + str(len(quotes)) + " quotes: (" + row[0] + ") " + row[1]
    else:
        return "Unknown command."

commands = {"quote": quote}
triggers = []

