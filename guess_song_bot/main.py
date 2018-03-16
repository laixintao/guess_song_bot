# -*- coding: utf-8 -*-

import os
import json
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
        self.right_song = await self.random_choice_song()
        self.piece = await self.random_piece()
        self.choices = await self.get_random_choices()
        self.tried_users = []
        self.object_share_link = BUCKET_PREFIX + self.piece
        return self


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
    logger.info("send choices, chat: {}, game: {}".format(chat, game))
    markup = {
        'keyboard': [
            [{'type': 'KeyboardButton',
              'text': choice.title
            }] for choice in game.choices],
        'one_time_keyboard': True,
        }
    chat.send_text(messages.guess_start, reply_markup=json.dumps(markup))


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


@bot.command("gameover")
async def game_over(chat, match):
    logger.info("/gameover command")
    if chat.id not in games:
        await chat.reply(messages.game_not_running)
        return
    current_game = games[chat.id]
    await chat.reply(messages.game_over_lose.format(current_game.right_song.title,
                                                    current_game.right_song.artist))
    games.pop(chat.id)


@bot.default
async def guess(chat, cq):
    """
    cq like this:
    {'message_id': 1250, 'from': {'id': 242165025, 'is_bot': False, 'first_name': 'caster', 'last_name': 'Le', 'username': 'untakename', 'language_code': 'zh-Hans-CN'}, 'chat': {'id': 242165025, 'first_name': 'caster', 'last_name': 'Le', 'username': 'untakename', 'type': 'private'}, 'date': 1521185990, 'text': 'Sleep, Baby, Sleep'}
    """
    logger.info("received message: {}".format(cq))
    if chat.id not in games:
        await chat.reply(messages.game_not_running)
        return

    current_game = games[chat.id]
    display_name = "{} {}".format(cq['from']['first_name'], cq['from']['last_name'])
    username = cq['from']['username']

    if username in current_game.tried_users:
        result = messages.you_are_tried.format(display_name)
        await chat.reply(result)
        return

    answer_text = cq['text']
    current_game.tried_users.append(username)

    if current_game.right_song.title == answer_text:
        result = messages.game_over_win.format(display_name,
                                               current_game.right_song.title,
                                               current_game.right_song.artist)
        await chat.reply(result)  # TODO no markup
        games.pop(chat.id)
    else:
        result = messages.answer_wrong.format(display_name)
        await chat.reply(result)
        current_game.tried_users.append(username)


def run_production():
    bot.run()


if __name__ == '__main__':
    bot.run(debug=True)
