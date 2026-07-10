import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wordle.game_logic import WordleLogic, TileResult  # noqa: F401


def make_logic(word="CRANE", num_rounds=6, num_chars=5, word_checker=lambda w: True):
    return WordleLogic(word, num_rounds, num_chars, word_checker)


def type_word(logic, word):
    for ch in word:
        logic.add_letter(ch)


def submit(logic, word):
    type_word(logic, word)
    return logic.submit_word()


G = TileResult.GREEN
Y = TileResult.YELLOW
R = TileResult.RED
E = TileResult.EMPTY
