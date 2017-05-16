# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation, unused-argument
# pylint: disable=redefined-outer-name, unused-variable
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import pymongo
import config_log
import messages
from song import get_random_choices, get_one_song


GAME_RUNNING = False
logger = logging.getLogger(__name__)
mongo = pymongo.MongoClient()
message_base = mongo['telegram']['messages']

game_info = {
    'db': 6,
    'choices': [],
    'answer': {}}

def start(bot, update):
    logger.info(update.message)
    update.message.reply_text(messages.start_message)


def new_game(bot, update):
    GAME_RUNNING = True
    logger.info(update.message)
    new_song = get_one_song()
    game_info['answer'] = new_song
    game_info['choices'] = get_random_choices()
    game_info['choices'].append(new_song['title'])
    update.message.reply_text(messages.new_game,
                              reply_markup=ReplyKeyboardMarkup(game_info['choices'],
                                                               on_time_keyboard=True))
    with open(new_song['piece_path'], 'rb') as piece_file:
    # with open('sounds/11_minute_song.mp3', 'rb') as piece_file:
        logger.debug("Sending song piece: {}".format(new_song['piece_path']))
        update.message.reply_audio(piece_file)


def test_send_song(bot, update):
    with open('11_minute_song.mp3', 'rb') as file:
        update.message.reply_audio(file)

def try_one_guess(bot, update):
    pass


def  setup_handler(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new_game', new_game))
    dp.add_handler(CommandHandler('test', test_send_song))


def main():
    with open('token.txt') as token_file:
        token = token_file.read().strip()
    updater = Updater(token)

    dp = updater.dispatcher
    setup_handler(dp)
    updater.start_polling()
    updater.idle()
