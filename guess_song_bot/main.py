# -*- coding: utf-8 -*-

import os
import logging
import random
import asyncio
from functools import partial

from aiotg import Bot

from guess_song_bot import messages
from guess_song_bot.utils import read_bucket, s3, BUCKET, BUCKET_PREFIX

bot = Bot(os.environ["API_TOKEN"])
games = {}  # chat.id: Game
logger = logging.getLogger(__name__)
songs = read_bucket()
loop = asyncio.get_event_loop()


class Game:
    """
    Status:
    1. ~~start~~
    2. uploaded
    3. publish_choices
    4. over
    """
    async def new(self):
        self.status = "start"
        self.right_song = await self.random_choice_song()
        self.piece = await self.random_piece()
        self.choices = await self.get_random_choices()
        self.tried_users = []
        self.object_share_link = BUCKET_PREFIX + self.piece
        return self


    def guess(self, username, choice):
        if choice == self.right_answer:
            self.status = "over"
            return True
        else:
            self.tried_users.append(username)

    async def random_choice_song(self):
        random_one = random.randrange(len(songs))
        song = songs[random_one]
        logger.info("Get random one index: {}, song: {}".format(random_one, song.title))
        return song

    async def random_piece(self):
        pieces = self.right_song.pieces
        result = random.sample(pieces, 1)[0]
        logger.info("random pieces, len: {}, result: {}".format(len(pieces), result))
        return result

    async def get_random_choices(self):
        """Need at least 4, in case of the right anwser in them"""
        choices = random.sample(songs, k=4)
        if self.right_song not in choices:
            choices[0] = self.right_song
        random.shuffle(choices)
        logger.info("shuffled choices: {}".format([song.title for song in choices]))
        return choices


def send_choices_callback(chat, game):
    logger.info("upload_song, chat: {}, game: {}".format(chat, game))
    chat.send_text(messages.guess_start)


@bot.command("whoami")
def whoami(chat, match):
    return chat.reply(chat.sender["id"])


@bot.command("song")
def send_song_link(chat, match):
    return chat.send_audio("https://telegram-bot.nyc3.digitaloceanspaces.com/song-piece-database/The%20Cardigans%20-%20Love%20Fool.mp3.mp3---(100000:110000)")


@bot.command("start")
async def start_new_game(chat, match):
    if chat.id in games:
        chat.reply(messages.game_already_running)
        return
    await chat.reply(messages.new_game)

    new_game = await Game().new()
    games[chat.id] = new_game
    logger.debug(games)
    logger.info("start to send audio link: {}".format(new_game.object_share_link))
    await chat.send_audio(new_game.object_share_link)

    send_choices = partial(send_choices_callback, chat, new_game)
    loop.call_later(3, send_choices)


def run_production():
    bot.run()


if __name__ == '__main__':
    bot.run(debug=True)
