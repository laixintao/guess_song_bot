# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import config_log
from bot import main


if __name__ == '__main__':
    main()
