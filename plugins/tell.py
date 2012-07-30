from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import re
import time

from botmily.db import db

def hook(nick, ident, host, message, bot, channel):
    if re.match('\.tell', message) is not None:
        db.execute("create table if not exists tells(nick_to, nick_from, message, time, channel)")
        components = message[6:].split(" ", 1)
        if len(components) == 1:
            return 'You need to enter a message'
        db.execute("insert into tells (nick_to, nick_from, message, time, channel) values (:nick_to, :nick_from, :message, :time, :channel)", {"nick_to": components[0].lower(), "nick_from": nick, "message": components[1], "time": time.time(), "channel": channel})
        db.commit()
        return "I'll pass that along."

    row = db.execute("select nick_to, nick_from, message, time, channel from tells where nick_to=:nick_to", {"nick_to": nick.lower()}).fetchone()
    if row:
        bot.notice(str(nick), str(row[1] + " said " + str(datetime.timedelta(seconds=(time.time() - row[3]))) + " ago in " + row[4] + " the following: " + row[2]))
        db.execute("delete from tells where nick_to=:nick_to and nick_from=:nick_from and message=:message and time=:time and channel=:channel", {"nick_to": row[0], "nick_from": row[1], "message": row[2], "time": row[3], "channel": row[4]})
        db.commit()

