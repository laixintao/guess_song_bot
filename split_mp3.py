# coding: utf-8

from __future__ import unicode_literals
import logging
from glob import glob
from pydub import AudioSegment

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

logger = logging.getLogger(__name__)

MP3_DIR = "{}"

def parse_mp3(mp3_filename):
    mp3_song = AudioSegment.from_mp3(mp3_filename)
    pices = mp3_song[::20*1000]  # 20s per pices
    for index, pice in zip(range(len(pices)), pices):
        logger.info("saving {}th audio to file.".format(index))
        print index,pice
        out_f = open("%s_minute_song.mp3" % index, 'wb')
        pice.export(out_f, format="mp3")


def get_all_mp3_files():
    return glob("*.mp3")

if __name__ == '__main__':
    logger.info("start processing...")
    for song in get_all_mp3_files():
        print song
        filename = MP3_DIR.format(song)
        logger.info("start parsing {}".format(filename))
        parse_mp3(filename)
