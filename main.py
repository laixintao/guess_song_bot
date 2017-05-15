# coding: utf-8
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                                  ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('use /new_song to start a new song')


def new_song(bot, update):
    with open('00001.mp3', 'rb') as mp3_file:
        update.message.reply_audio(mp3_file)


def main():
    # Create the EventHandler and pass it your bot's token.
    token = ''
    with open('token.txt') as token_file:
        token = token_file.read().strip()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new_song', new_song))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

