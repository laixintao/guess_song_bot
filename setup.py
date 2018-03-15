# -*- coding: utf-8 -*-

from distutils.core import setup

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='guess_song_bot',
    version='0.0.2',
    description='Telegram bot, guess song game',
    author='laixintao',
    author_email='laixintao1995@163.com',
    url='https://www.python.org/',
    entry_points={
        'console_scripts': [
            'cut_song = guess_song_bot.split_mp3:main'
        ]
    },
    packages=['guess_song_bot'],
)
