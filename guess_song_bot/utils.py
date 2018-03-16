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
song_name_re = re.compile(r"song-piece-database/(.*) - (.*).mp3")
logger = logging.getLogger(__name__)


class Song:
    def __init__(self, artist, title):
        self.pieces = []
        self.artist = artist
        self.title = title

    def __eq__(self, other):
        return self.artist == other.artist and self.title == other.title


def read_bucket():
    """List all songs' name from bucket"""
    logger.info("start loading songs from s3...")
    objects_all = s3.list_objects(BUCKET, "song-piece-database/", False)
    songs = []
    for obj in objects_all:
        song_name = obj.object_name
        artist_title = song_name_re.match(song_name).groups()
        new_song = Song(*artist_title)
        if new_song in songs:
            new_song = songs[songs.index(new_song)]
        else:
            songs.append(new_song)
        new_song.pieces.append(song_name)

    logger.info("loading finish, {} songs".format(len(songs)))
    return songs
