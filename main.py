# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import config_log


def start(bot, update):
    update.message.reply_text('use /new_song to start a new song')


def new_song(bot, update):
    with open('00001.mp3', 'rb') as mp3_file:
        update.message.reply_audio(mp3_file)


def main():


if __name__ == '__main__':
    main()
