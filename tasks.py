# -*- coding: utf-8 -*-

""" celery tasks """

from __future__ import unicode_literals
from telegram.bot import Bot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from celery import Celery
from utils import get_token

app = Celery('guess_song_bot', broker='redis://localhost')

@app.task
def send_message(chat_id, message, key_board='remove', key_board_choices=None):
    if key_board == 'remove':
        key_board = ReplyKeyboardRemove()
    elif key_board == 'choice':
        key_board = ReplyKeyboardMarkup(key_board_choices, on_time_keyboard=True)
    bot = Bot(get_token())
    bot.send_message(chat_id, message, reply_markup=key_board)


@app.task
def send_audio(chat_id, audio, key_board='remove', key_board_choices=None):
    if key_board == 'remove':
        key_board = ReplyKeyboardRemove()
    elif key_board == 'choice':
        key_board = ReplyKeyboardMarkup(key_board_choices, on_time_keyboard=True)
    bot = Bot(get_token())
    bot.send_message(chat_id, audio, reply_markup=key_board)
