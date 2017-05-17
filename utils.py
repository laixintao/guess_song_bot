# coding:utf-8

import redis
import pymongo
from functools import wraps
import config_log
import logging


logger = logging.getLogger(__name__)

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
        except Exception as e:
            logger.warn(e)
    return wrapper
