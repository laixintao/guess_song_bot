# coding: utf-8
# pylint: disable=invalid-name

"Conse messages"

# start game
new_game = """新游戏开始！正在生成题目...正在上传音乐片段...15s之后发布选项..."""
guess_start = """听过这首歌吗？现在可以根据键盘的选项作答了!"""

game_already_running = """当前游戏正在进行，不能开启新的游戏。"""

# guess
game_not_running = """目前没有游戏正在进行，使用 /start 开启一个新游戏!"""
answer_wrong = """{0}猜错了！游戏继续进行。{0}不能继续再猜了"""
you_are_tried = """{}已经猜过了，没有机会再猜了"""

# over
game_over_lose = """游戏结束，正确答案是{}, 歌手{}"""
game_over_win = """{}猜对了！游戏结束, 正确答案是{}, 歌手是{}"""
