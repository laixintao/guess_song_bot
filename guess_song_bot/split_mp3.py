#!/usr/bin/python
# coding: utf-8

import sys
import re
from io import BytesIO
from pathlib import Path
import logging
import concurrent.futures

from pydub import AudioSegment
import taglib

from guess_song_bot.utils import s3, BUCKET

LENGTH_PER_PIECE = 19 * 1000
SONG_FOLDER = "song-piece-database"

logger = logging.getLogger(__name__)
name_re = re.compile(r"(.*)\.mp3")


def parse_mp3(song):
    mp3_song = AudioSegment.from_mp3(str(song.absolute()))
    song_info = {}
    filename = song.name
    song_info = str(taglib.File(str(song.absolute())).tags)
    logger.info("Song: {}, info: {}".format(filename, song_info))
    print("start to upload: {}".format(filename))

    for index in range(0, len(mp3_song), LENGTH_PER_PIECE):
        start = index
        end = LENGTH_PER_PIECE + index
        if end > len(mp3_song):
            break
        piece = mp3_song[start: end]
        out_filename = "{}/{}---({}:{})".format(SONG_FOLDER, filename, start, end)
        raw_data = BytesIO()
        piece.export(raw_data)
        s3.put_object(BUCKET, out_filename, raw_data,
                      len(raw_data.getbuffer()), 'audio/mpeg',
                      metadata={
                          'x-amz-meta-tag': song_info,
                          'x-amz-acl': 'public-read',
                      })
    song_prefix = name_re.match(filename).group(1)
    new_abs_name = song.parent / "{}-DONE.mp3".format(song_prefix)
    song.rename(str(new_abs_name))


def get_all_mp3_files(song_path):
    files = [f for f in song_path.iterdir() if not f.name.endswith("DONE.mp3")]
    return files


def main():
    path = Path(sys.argv[1])
    logger.info("Path: {}".format(path))
    songs = get_all_mp3_files(path)
    logger.info("Song list: {}".format(songs))

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    for song in songs:
        executor.submit(parse_mp3, song)


if __name__ == '__main__':
    main()
