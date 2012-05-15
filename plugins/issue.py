from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from botmily.db import db

def hook(nick, ident, host, message):
    if re.match('.issue', message) is None:
        return None

    db.execute("create table if not exists issues(id integer primary key, issue)")
    issue = message[7:]
    db.execute("insert into issues(id, issue) values(null, :issue)", {"issue": issue})
    db.commit()
    return 'Thanks for your worthless complaint.'
