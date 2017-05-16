# coding: utf-8
# pylint: disable=missing-docstring, unused-import, import-error,
# pylint: disable=invalid-name, logging-format-interpolation
from __future__ import unicode_literals

import logging
import os
import time

from glob import glob
from pydub import AudioSegment
import taglib
import config_log
import pymongo

LENGTH_PER_PIECE = 30*1000
MP3_FILE_PATH = 'mp3/'
EXPORT_PIECES_PATH = os.getcwd() + '/sounds/'

logger = logging.getLogger(__name__)
mongo_client = pymongo.MongoClient()
song_base = mongo_client['guess_song']['song']


def check_song_in_database(filename):
    basename = os.path.basename(filename)
    result = song_base.find({'filename': basename})
    if not result:
        return False
    return True


def parse_mp3(mp3_filename):
    mp3_song = AudioSegment.from_mp3(mp3_filename)
    song_length = len(mp3_song) / (LENGTH_PER_PIECE)
    song_info = {}
    song_info['filename'] = os.path.basename(mp3_filename)
    song_info['tags'] = get_info(mp3_filename)
    song_info['song_length'] = len(mp3_song)
    song_info['total_pieces'] = song_length
    pieces_filename = []
    for index in range(song_length):
        piece = mp3_song[index*LENGTH_PER_PIECE:(index+1)*LENGTH_PER_PIECE]
        out_filename = "{}.mp3".format(EXPORT_PIECES_PATH+str(time.time()))
        out_f = open(out_filename, 'wb')
        piece.export(out_f, format="mp3")
        logger.info('{} ({}/{}) piece of {} has been saved'.format(
            out_filename, index+1, song_length, song_info['filename']))
        pieces_filename.append(out_filename)
    song_info['pieces'] = pieces_filename
    song_info['created_at'] = time.time()
    song_base.update(song_info, song_info, upsert=True)


def get_all_mp3_files():
    return glob("{}*.mp3".format(MP3_FILE_PATH))


def parsing_all_mp3_files():
    all_songs = get_all_mp3_files()
    total_songs = len(all_songs)
    for index, song in zip(range(1, total_songs+1), all_songs):
        abs_song_path = os.path.abspath(song)
        if check_song_in_database(song):
            logger.warn("{} already in database, skip this song. progress {}/{}".format(
                os.path.basename(song), index, total_songs))
            continue
        logger.info("Start parsing {}, progreess {}/{}".format(abs_song_path, index, total_songs))
        parse_mp3(abs_song_path)


def get_info(filename):
    song = taglib.File(filename)
    return song.tags


if __name__ == '__main__':
    parsing_all_mp3_files()
