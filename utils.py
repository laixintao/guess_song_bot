# coding:utf-8

import logging
import traceback
from functools import wraps
import redis
import pymongo
import config_log


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
        except:
            traceback.print_stack()
    return wrapper
