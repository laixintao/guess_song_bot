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

tried_users = []

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
    tried_users = []
    new_song = get_one_song()
    game_info['answer'] = new_song
    game_info['choices'] = get_random_choices(new_song['title'])
    game_info['choices'].append(new_song['title'])
    update.message.reply_text(messages.new_game,
                              reply_markup=ReplyKeyboardMarkup(game_info['choices'],
                                                               on_time_keyboard=True))
    with open(new_song['piece_path'], 'rb') as piece_file:
        logger.debug("Sending song piece: {}".format(new_song['piece_path']))
        update.message.reply_audio(piece_file)


def test_send_song(bot, update):
    pass


def try_one_guess(bot, update):
    logger.info(update.message)
    if not GAME_RUNNING:
        update.message.reply_text(messages.game_not_running)
        return
    answer = update.message.text
    user = update.message.from_user
    if user in tried_users:
        update.message.reply_text(messages.you_are_tried.format(user))
        return
    tried_users.append(user)
    if answer == game_info['answer']['title']:
        update.message.reply_text(messages.answer_right.format(user))
    else:
        update.message.reply_text(messages.answer_wrong.format(user))
        GAME_RUNNING = False



def  setup_handler(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new_game', new_game))
    dp.add_handler(CommandHandler('test', test_send_song))
    dp.add_handler(MessageHandler(Filters.photo, try_one_guess))


def main():
    with open('token.txt') as token_file:
        token = token_file.read().strip()
    updater = Updater(token)

    dp = updater.dispatcher
    setup_handler(dp)
    updater.start_polling()
    updater.idle()
