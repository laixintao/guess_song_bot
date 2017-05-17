# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation, unused-argument
# pylint: disable=redefined-outer-name, unused-variable
from __future__ import unicode_literals
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import config_log
import messages
from song import get_random_choices, get_one_song
from utils import mongo
from utils import redis_instance as redis


logger = logging.getLogger(__name__)
message_base = mongo['telegram']['messages']
GAME_RUNNING_KEY = 'guess_song_bot:bot:game_is_running'
TRIED_USERS_KEY = 'guess_song_bot:bot:tried_users'


game_info = {
    'db': 6,
    'choices': [],
    'answer': {}}


def game_is_running():
    return redis.get(GAME_RUNNING_KEY)

def set_game_running():
    redis.set(GAME_RUNNING_KEY, True)


def game_over():
    redis.set(GAME_RUNNING_KEY, False)

def start(bot, update):
    logger.info(update.message)
    update.message.reply_text(messages.start_message)


def new_game(bot, update):
    set_game_running()
    logger.info(update.message)
    tried_users = []
    new_song = get_one_song()
    game_info['answer'] = new_song
    game_info['choices'] = get_random_choices(new_song['title'])
    update.message.reply_text(messages.new_game,
                              reply_markup=ReplyKeyboardMarkup(game_info['choices'],
                                                               on_time_keyboard=True))
    with open(new_song['piece_path'], 'rb') as piece_file:
        logger.debug("Sending song piece: {}".format(new_song['piece_path']))
        update.message.reply_audio(piece_file)


def test_send_song(bot, update):
    pass


def get_tried_users():
    "return tried user_id"
    users = redis.lrange(TRIED_USERS_KEY, 0, -1)
    return [int(uid) for uid in users]

def try_one_guess(bot, update):
    logger.info(update.message)
    user_first_name = update.message.from_user.first_name
    logger.info("New try: {}, from: {}".format(update.message.text, update.message.from_user.first_name))
    if not game_is_running():
        update.message.reply_text(messages.game_not_running)
    answer = update.message.text
    user = update.message.from_user
    if user.id in get_tried_users():
        update.message.reply_text(messages.you_are_tried.format(user_first_name))
        return
    redis.lpush(TRIED_USERS_KEY, user.id)
    if answer == game_info['answer']['title']:
        update.message.reply_text(messages.answer_right.format(user_first_name))
    else:
        update.message.reply_text(messages.answer_wrong.format(user_first_name))
        game_over()


def setup_handler(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new_game', new_game))
    dp.add_handler(CommandHandler('test', test_send_song))
    dp.add_handler(MessageHandler(Filters.text, try_one_guess))


def main():
    with open('token.txt') as token_file:
        token = token_file.read().strip()
    updater = Updater(token)

    dp = updater.dispatcher
    setup_handler(dp)
    updater.start_polling()
    updater.idle()
