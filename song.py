# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation
import logging
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import config_log
import pymongo

mongo = pymongo.MongoClient()
song_base = mongo['guess_song']['song']

logger = logging.getLogger(__name__)

def get_song_total_number():
    return song_base.count()


def get_one_song():
    skip = random.randint(0, get_song_total_number()-1)
    result = song_base.find()[skip]
    song_info = {
        'title': result['tags']['TITLE'],
        'artist': result['tags']['ARTIST'],
        'album': result['tags']['ALBUM']}
    logger.info('Get song info {}'.format(song_info))
    pieces = result['pieces']
    random_piece = random.randint(0, len(pieces)-1)
    song_info['piece_path'] = pieces[random_piece]
    return song_info


def get_random_choices(right_answer):
    choices = [right_answer, ]
    while len(choices) < 2:
        skip = random.randint(0, get_song_total_number()-1)
        result = song_base.find()[skip]
        song = result['tags']['TITLE']
        if song not in choices:
            choices.append(song)
    return choices

if __name__ == '__main__':
    for _ in range(10):
        get_one_song()
