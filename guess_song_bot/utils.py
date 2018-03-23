# -*- coding: utf-8 -*-

import os
import re
import urllib3
from urllib3 import PoolManager
import logging

from minio import Minio

SECRET = os.environ['SECRET']
KEY = os.environ['KEY']
BUCKET = "telegram-bot"
BUCKET_PREFIX = 'https://telegram-bot.nyc3.digitaloceanspaces.com/'

urllib3.disable_warnings()
manager = PoolManager(10, maxsize=100)
s3 = Minio('nyc3.digitaloceanspaces.com',
           access_key=KEY,
           secret_key=SECRET,
           secure=True,
           http_client=manager)
logger = logging.getLogger(__name__)


class Song:
    def __init__(self, artist, title, album):
        self.pieces = []
        self.artist = artist
        self.title = title
        self.album = album

    def __eq__(self, other):
        return self.artist == other.artist and self.title == other.title and self.album == other.album

    def __str__(self):
        return "MUSIC-{} by {} <<{}>>-".format(self.title, self.artist, self.album)


def read_bucket():
    """List all songs' name from bucket"""
    logger.info("start loading songs from s3...")
    objects_all = s3.list_objects(BUCKET, "", False)
    songs = []
    for obj in objects_all:
        logger.info(obj.object_name)
        obj = s3.stat_object(BUCKET, obj.object_name)
        artist = obj.metadata['x-amz-meta-artist']
        album = obj.metadata['x-amz-meta-album']
        title = obj.metadata['x-amz-meta-title']
        new_song = Song(artist, title, album)

        if new_song in songs:
            new_song = songs[songs.index(new_song)]
        else:
            songs.append(new_song)
        new_song.pieces.append(obj.object_name)
        logger.info(new_song)


    logger.info("loading finish, {} songs".format(len(songs)))
    return songs
