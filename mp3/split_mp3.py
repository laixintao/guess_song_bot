# coding: utf-8
from __future__ import unicode_literals

import logging

from glob import glob
from pydub import AudioSegment


LENGTH_PER_PIECE = 20*1000
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

logger = logging.getLogger(__name__)


def parse_mp3(mp3_filename):
    mp3_song = AudioSegment.from_mp3(mp3_filename)
    song_length = len(mp3_song) / (LENGTH_PER_PIECE)
    logger.info('song pieces: {}'.format(song_length))
    for index in range(song_length-1):
        piece = mp3_song[index*LENGTH_PER_PIECE:(index+1)*LENGTH_PER_PIECE]
        out_f = open("%s_minute_song.mp3" % index, 'wb')
        piece.export(out_f, format="mp3")
        logger.info('piece {} has been saved'.format(out_f))


def get_all_mp3_files():
    return glob("*.mp3")


if __name__ == '__main__':
    for song in get_all_mp3_files():
        logger.info("start parsing {}".format(song))
        parse_mp3(song)
