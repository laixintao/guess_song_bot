#!/usr/bin/python
# coding: utf-8

import sys
import re
from io import BytesIO
from pathlib import Path
import logging
import concurrent.futures
import uuid

from pydub import AudioSegment
import taglib

from guess_song_bot.utils import s3, BUCKET, read_bucket

LENGTH_PER_PIECE = 20 * 1000
SONG_FOLDER = "song-piece-database"

logger = logging.getLogger(__name__)
name_re = re.compile(r"(.*)\.mp3")


def parse_mp3(song):
    mp3_song = AudioSegment.from_mp3(str(song.absolute()))
    song_info = {}
    filename = song.name
    song_info = taglib.File(str(song.absolute())).tags
    logger.info("tags: {}".format(song_info))
    meta_info = {
        'x-amz-meta-album': song_info['ALBUM'][0],
        'x-amz-meta-artist': song_info['ARTIST'][0],
        'x-amz-meta-title': song_info['TITLE'][0],
        'x-amz-acl': 'public-read',
    }
    logger.info("song meta info: {}".format(meta_info))

    for index in range(0, len(mp3_song), LENGTH_PER_PIECE):
        start = index
        end = LENGTH_PER_PIECE + index
        if end > len(mp3_song):
            break
        piece = mp3_song[start: end]
        out_filename = str(uuid.uuid4().int)
        raw_data = BytesIO()
        piece.export(raw_data)
        try:
            upload_result = s3.put_object(BUCKET, out_filename, raw_data,
                                          len(raw_data.getbuffer()), 'audio/mpeg', metadata=meta_info)
        except UnicodeEncodeError:
            logger.error("Can not upload: {} {}".format(filename, index))
        else:
            logger.info("Upload finished: {}".format(upload_result))


def get_all_mp3_files(song_path):
    files = [f for f in song_path.iterdir()]
    return files


def main():
    exists_songs = read_bucket()
    path = Path(sys.argv[1])
    logger.info("Path: {}".format(path))
    songs = get_all_mp3_files(path)
    logger.info("Song list: {}".format(songs))

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    for song in songs:
        is_exist = False
        for exist in exists_songs:
            if exist.title in str(song) and exist.artist in str(song):
                is_exist = True
                break
        if is_exist:
            logger.info("{} already exists.".format(song))
            continue
        executor.submit(parse_mp3, song)


if __name__ == '__main__':
    main()
