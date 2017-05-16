# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation, unused-argument
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import pymongo
import config_log
import messages


GAME_RUNNING = False
logger = logging.getLogger(__name__)
message_base = mongo['telegram']['messages']

game_info = {
        'db': 6,
        'choices': [],
        'answer': {}
        }

def start(bot, update):
    logger.info(update.message)
    update.message.reply_text(messages.start_message)


def new_game(bot, update):
    GAME_RUNNING = True
    logger.info(update.message)
    new_song = get_one_song()
    game_info['answer'] = new_song
    game_info['choices'] = get_choices()
    game_info['choices'].append(:wq

    update.message.reply_text(messages.new_game)


def try_one_guess(bot, update):
    pass


def setup_handler(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new_game', new_game))


def main():
    with open('token.txt') as token_file:
        token = token_file.read().strip()
    updater = Updater(token)

    dp = updater.dispatcher
    updater.start_polling()
    updater.idle()
