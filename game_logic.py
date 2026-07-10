from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional


class TileResult(Enum):
    EMPTY = "empty"
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


@dataclass
class SubmitResult:
    scores: List[TileResult]
    won: bool
    game_over: bool
    round_index: int  # 0-based index of the round just submitted (pre-advance)


class WordleLogic:
    def __init__(
            self,
            word: str,
            num_rounds: int = 6,
            num_chars: int = 5,
            word_checker: Callable[[str], bool] = None,
    ):
        self._num_rounds = num_rounds
        self._num_chars = num_chars
        self._word_checker = word_checker if word_checker is not None else lambda w: True
        self._tiles: List[List[Optional[str]]] = [
            [None] * num_chars for _ in range(num_rounds)
        ]
        self._color_tiles: List[List[TileResult]] = [
            [TileResult.EMPTY] * num_chars for _ in range(num_rounds)
        ]
        self._round = 0
        self._char = 0
        self._game_over = False
        self._won = False
        self._invalid_word = False
        self._set_word(word)

    def _set_word(self, word: str) -> None:
        self._word_str = word.upper()
        self._word = list(self._word_str)

    def add_letter(self, letter: str) -> bool:
        if not self.can_add_letter():
            return False
        self._tiles[self._round][self._char] = letter.upper()
        self._char += 1
        return True

    def delete_letter(self) -> bool:
        if not self.can_delete_letter():
            return False
        self._char -= 1
        self._tiles[self._round][self._char] = None
        self._invalid_word = False
        return True

    def can_add_letter(self) -> bool:
        return not self._game_over and self._round < self._num_rounds and self._char < self._num_chars

    def can_delete_letter(self) -> bool:
        return not self._game_over and self._round < self._num_rounds and self._char > 0

    def can_submit_word(self) -> bool:
        if self._game_over or self._round >= self._num_rounds or self._char != self._num_chars:
            return False
        word = ''.join(self._tiles[self._round])
        is_word = self._word_checker(word)
        if not is_word:
            self._invalid_word = True
        return is_word

    def submit_word(self) -> Optional[SubmitResult]:
        if not self.can_submit_word():
            return None

        current_round = self._round
        scores = []

        for i in range(self._num_chars):
            if self._tiles[self._round][i] == self._word[i]:
                result = TileResult.GREEN
            elif self._tiles[self._round][i] in self._word_str and self.check_yellow(i):
                result = TileResult.YELLOW
            else:
                result = TileResult.RED
            scores.append(result)
            self._color_tiles[self._round][i] = result

        won = self._tiles[self._round] == self._word

        if not won:
            self._round += 1
            self._char = 0

        game_over = won or self._round >= self._num_rounds

        if game_over:
            self._game_over = True
            self._won = won

        return SubmitResult(
            scores=scores,
            won=won,
            game_over=game_over,
            round_index=current_round,
        )

    def check_yellow(self, i: int) -> bool:
        target = self._tiles[self._round][i]
        for ind in range(len(self._word_str)):
            if self._word_str[ind] == target and self._tiles[self._round][ind] != target:
                return True
        return False

    def reset(self, word: str) -> None:
        self._tiles = [[None] * self._num_chars for _ in range(self._num_rounds)]
        self._color_tiles = [[TileResult.EMPTY] * self._num_chars for _ in range(self._num_rounds)]
        self._round = 0
        self._char = 0
        self._game_over = False
        self._won = False
        self._invalid_word = False
        self._set_word(word)

    @property
    def tiles(self) -> List[List[Optional[str]]]:
        return self._tiles

    @property
    def color_tiles(self) -> List[List[TileResult]]:
        return self._color_tiles

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def invalid_word(self) -> bool:
        return self._invalid_word

    @property
    def round(self) -> int:
        return self._round

    @property
    def char(self) -> int:
        return self._char

    @property
    def word_str(self) -> str:
        return self._word_str

    @property
    def num_rounds(self) -> int:
        return self._num_rounds

    @property
    def num_chars(self) -> int:
        return self._num_chars
