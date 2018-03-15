# -*- coding: utf-8 -*-

import os
import re
import urllib3
from urllib3 import PoolManager

from minio import Minio

SECRET = os.environ['SECRET']
KEY = os.environ['KEY']
BUCKET = "telegram-bot"

urllib3.disable_warnings()
manager = PoolManager(10, maxsize=100)
s3 = Minio('nyc3.digitaloceanspaces.com',
           access_key=KEY,
           secret_key=SECRET,
           secure=True,
           http_client=manager)
song_name_re = re.compile(r"song-piece-database/(.*) - (.*).mp3")


def list_songs():
    """List all songs' name from bucket"""
    songs = s3.list_objects(BUCKET, "song-piece-database/", False)
    uniques_songs = []
    for song in songs:
        song_name = song.object_name
        artist, title = song_name_re.match(song_name).groups()
        if title not in uniques_songs:
            uniques_songs.append(title)
    return uniques_songs


if __name__ == '__main__':
    print(list_songs())
