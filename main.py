from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from botmily import bot
from botmily import config
from botmily import db

if __name__ == '__main__':
    print("Starting the bot")
    config.getConfig()
    db.connect()
    bot.bot()

