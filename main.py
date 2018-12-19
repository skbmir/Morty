#!/usr/bin/env python3

import os
import time
import re
from slackclient import SlackClient
from morty import Morty

if __name__ == '__main__':
    # get bot token
    token_file = open('bot_token', 'r')
    bot_token = token_file.read()

    morty = Morty(bot_token)

    if morty.connect():
        morty.main_loop()