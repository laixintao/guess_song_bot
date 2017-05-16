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


def start(bot, update):
    logger.info(update.message)
    update.reply_text(messages.start_message)


def new_game(bot, update):
    pass


def try_one_guess(bot, update):
    pass


def main():
    with open('token.txt') as token_file:
        token = token_file.read().strip()
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()
