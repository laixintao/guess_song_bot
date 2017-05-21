# -*- coding: utf-8 -*-

""" celery tasks """

from __future__ import unicode_literals
from telegram.bot import Bot
from celery import Celery
from utils import get_token

app = Celery('guess_song_bot', broker='redis://localhost')

@app.task
def send_message(chat_id, message, key_board):
    bot = Bot(get_token())
    bot.send_message(chat_id, message, reply_markup=key_board)
