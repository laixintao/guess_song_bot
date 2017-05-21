# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation, unused-argument
# pylint: disable=redefined-outer-name, unused-variable
from __future__ import unicode_literals
import logging
import json
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Chat)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import config_log
import messages
from song import get_random_choices, get_one_song
from utils import mongo, log_exception, get_token
from utils import redis_instance as redis
from tasks import  send_message


logger = logging.getLogger(__name__)
message_base = mongo['telegram']['messages']
GAME_RUNNING_KEY = 'guess_song_bot:bot:chat-{}:game_is_running'
TRIED_USERS_KEY = 'guess_song_bot:bot:chat-{}:tried_users'
GAME_INFO_KEY = 'guess_song_bot:bot:chat-{}:game_info'


def game_is_running(chat_id):
    return redis.get(GAME_RUNNING_KEY.format(chat_id)) == b'True'

def set_game_running(chat_id):
    redis.set(GAME_RUNNING_KEY.format(chat_id), True)
    redis.delete(TRIED_USERS_KEY.format(chat_id))


@log_exception
def game_over(chat_id, update, win):
    game_info = json.loads(redis.get(GAME_INFO_KEY.format(chat_id)).decode('utf-8'))
    logger.info("game over")
    redis.delete(GAME_RUNNING_KEY.format(chat_id))
    redis.delete(TRIED_USERS_KEY.format(chat_id))
    if not win:
        update.message.reply_text(messages.game_over_lose.format(**game_info['answer']),
                                  reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text(messages.game_over_win.format(**game_info['answer']),
                                  reply_markup=ReplyKeyboardRemove())


def set_game_over(bot, update):
    chat_id = update.message.chat_id
    if not game_is_running(chat_id):
        update.messages.reply_text(messages.game_not_running)
        return
    game_over(chat_id, update, False)


def start(bot, update):
    logger.info(update.message)
    update.message.reply_text(messages.start_message)


@log_exception
def new_game(bot, update):
    chat_id = update.message.chat_id
    if game_is_running(chat_id):
        update.message.reply_text(messages.game_already_running)
        return

    set_game_running(chat_id)
    new_song = get_one_song()
    choices = get_random_choices(new_song['title'])
    game_info = {
        'chat_id': chat_id,
        'db': 6,
        'type': update.message.chat.type,
        'choices': choices,
        'answer': new_song}
    redis.set(GAME_INFO_KEY.format(chat_id), json.dumps(game_info))
    logger.debug("Set {} to {}".format(GAME_INFO_KEY.format(chat_id), game_info))

    logger.debug("Async message sent")
    with open(new_song['piece_path'], 'rb') as piece_file:
        logger.debug("Sending song piece: {}".format(new_song['piece_path']))
        update.message.reply_text(messages.new_game)
        update.message.reply_audio(piece_file)


def test_send_song(bot, update):
    pass


def get_tried_users(chat_id):
    "return tried user_id"
    users = redis.lrange(TRIED_USERS_KEY.format(chat_id), 0, -1)
    return [int(uid) for uid in users]

@log_exception
def try_one_guess(bot, update):
    logger.info(update.message)
    chat_id = update.message.chat_id
    user_first_name = update.message.from_user.first_name
    logger.info("New try: {}, from: {}".format(update.message.text, user_first_name))
    # check if game is running
    logger.info("Game running info: {}".format(game_is_running(chat_id)))
    if not game_is_running(chat_id):
        update.message.reply_text(messages.game_not_running)
        return
    # check if user has tried
    user = update.message.from_user
    if user.id in get_tried_users(chat_id):
        update.message.reply_text(messages.you_are_tried.format(user_first_name))
        return
    redis.lpush(TRIED_USERS_KEY.format(chat_id), user.id)
    # check if answer is right
    answer = update.message.text
    game_info = json.loads(redis.get(GAME_INFO_KEY.format(chat_id)).decode('utf-8'))
    if answer == game_info['answer']['title'][0]:
        update.message.reply_text(messages.answer_right.format(user_first_name),
                                  reply_markup=ReplyKeyboardRemove())
        game_over(chat_id, update, True)
    else:
        update.message.reply_text(messages.answer_wrong.format(user_first_name))
        if game_info['type'] == Chat.PRIVATE:
            game_over(chat_id, update, False)


def setup_handler(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new_game', new_game))
    dp.add_handler(CommandHandler('test', test_send_song))
    dp.add_handler(CommandHandler('game_over', set_game_over))
    dp.add_handler(MessageHandler(Filters.text, try_one_guess))


def main():
    token = get_token()
    logger.info("get token: {}".format(token))
    updater = Updater(token)
    dp = updater.dispatcher
    setup_handler(dp)
    updater.start_polling()
    updater.idle()
