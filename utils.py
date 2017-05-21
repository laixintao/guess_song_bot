# coding:utf-8

import logging
import traceback
from functools import wraps
import redis
import pymongo
import config_log


logger = logging.getLogger(__name__)
BOT_TOKEN_KEY = 'guess_song_bot:bot:bot-token'

def get_redis():
    """return a redis instance"""
    return redis.Redis()


def get_mongo():
    """return a mongo instance"""
    mongo = pymongo.MongoClient()
    return mongo


redis_instance = get_redis()
mongo = get_mongo()

def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            traceback.print_stack()
    return wrapper


def set_token():
    logger.info("Get token from token.txt")
    with open('token.txt') as token_file:
        token = token_file.read().strip()
        redis_instance.set(BOT_TOKEN_KEY, token)
    return token


def get_token():
    token = redis_instance.get(BOT_TOKEN_KEY)
    if not token:
        token = set_token()
    return token
