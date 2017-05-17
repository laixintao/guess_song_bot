# coding:utf-8

import redis
import pymongo


def get_redis():
    """return a redis instance"""
    return redis.Redis()


def get_mongo():
    """return a mongo instance"""
    mongo = pymongo.MongoClient()
    return mongo


redis_instance = get_redis()
mongo = get_mongo()
