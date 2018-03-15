import os
from aiotg import Bot

bot = Bot(os.environ["API_TOKEN"])
game = {}


class Game:
    """
    Status:
    1. start
    2. uploaded
    3. publish_choices
    4. over
    """
    def __init__(self):
        self.status = "start"
        self.right_answer = ""
        self.choices = []
        self.tried_users = []

    def guess(self, username, choice):
        if choice == self.right_answer:
            self.status = "over"
            return True
        else:
            self.tried_users.append(username)

@bot.command("whoami")
def whoami(chat, match):
    return chat.reply(chat.sender["id"])


@bot.command("song")
def send_song_link(chat, match):
    return chat.send_audio("https://telegram-bot.nyc3.digitaloceanspaces.com/song-piece-database/The%20Cardigans%20-%20Love%20Fool.mp3.mp3---(100000:110000)")


if __name__ == '__main__':
    bot.run(debug=True)
