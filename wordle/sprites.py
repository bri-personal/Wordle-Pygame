from enum import Enum

import enchant
import pygame

from .game_logic import TileResult, WordleLogic
from .settings import *

_TILE_RESULT_TO_COLOR = {
    TileResult.EMPTY: WHITE,
    TileResult.GREEN: GREEN,
    TileResult.YELLOW: YELLOW,
    TileResult.RED: RED,
}


class Page(Enum):
    PLAY = 'play'
    END = 'end'
    STATS = 'stats'


# show text on surface with parameters given
def draw_text(surface: pygame.Surface, text: str, size: int, color: tuple[int, int, int], x: int, y: int,
              orientation: str):
    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if orientation == 'topleft':
        text_rect.topleft = (x, y)
    elif orientation == 'midtop':
        text_rect.midtop = (x, y)
    elif orientation == 'center':
        text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


# classes
class Board(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int, word: str, num_rounds: int = 6, num_chars: int = 5):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.BORDER = 10
        self.TILE_SIZE = (SIDE - (max(num_chars, num_rounds) + 1) * self.BORDER) // max(num_chars, num_rounds)

        # create game board
        self.image = pygame.Surface(
            (WIDTH, (max(num_chars, num_rounds) + 1) * self.BORDER + self.TILE_SIZE * max(num_chars, num_rounds)))
        self.image.fill(BG_COLOR_1)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.logic = WordleLogic(
            word=word,
            num_rounds=num_rounds,
            num_chars=num_chars,
            word_checker=enchant.Dict("en_US").check,
        )

    @property
    def word_str(self):
        return self.logic.word_str

    @property
    def round(self):
        return self.logic.round

    @property
    def num_rounds(self):
        return self.logic.num_rounds

    # update tiles on board on GUI with letters and colors
    def update(self):
        tiles = self.logic.tiles
        color_tiles = self.logic.color_tiles
        num_chars = self.logic.num_chars
        current_round = self.logic.round
        text_color = RED if self.logic.invalid_word else BLACK

        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                start_x = WIDTH // 2 - (
                        int(num_chars / 2 * self.TILE_SIZE) + (num_chars // 2 + 1) * self.BORDER)

                pygame.draw.rect(self.image, _TILE_RESULT_TO_COLOR[color_tiles[i][j]],
                                 (start_x + self.BORDER + j * (self.TILE_SIZE + self.BORDER),
                                  self.BORDER + i * (self.TILE_SIZE + self.BORDER), self.TILE_SIZE, self.TILE_SIZE))
                if tiles[i][j] is not None:
                    if i == current_round:
                        draw_text(self.image, tiles[i][j], 32, text_color,
                                  start_x + self.BORDER + j * (self.TILE_SIZE + self.BORDER) + self.TILE_SIZE / 2,
                                  self.BORDER + i * (self.TILE_SIZE + self.BORDER) + self.TILE_SIZE / 2, 'center')
                    else:
                        draw_text(self.image, tiles[i][j], 32, BLACK,
                                  start_x + self.BORDER + j * (self.TILE_SIZE + self.BORDER) + self.TILE_SIZE / 2,
                                  self.BORDER + i * (self.TILE_SIZE + self.BORDER) + self.TILE_SIZE / 2, 'center')

    def add_letter(self, letter):
        self.logic.add_letter(letter)

    def delete_letter(self):
        self.logic.delete_letter()

    def submit_word(self):
        result = self.logic.submit_word()
        if result is None:
            return

        tiles = self.logic.tiles
        for i, score in enumerate(result.scores):
            color = _TILE_RESULT_TO_COLOR[score]
            self.game.update_letter_button(tiles[result.round_index][i], color)

        if result.game_over:
            self.game.page = Page.END
            stat_idx = result.round_index if result.won else self.logic.num_rounds
            self.game.stats[stat_idx] += 1
            self.game.stat_total += 1
            stats_str = ''
            for stat in self.game.stats:
                stats_str += str(stat) + '\n'
            with open('../stats.txt', 'w') as file:
                file.write(stats_str)

    def reset(self, word):
        self.logic.reset(word)


class Button:
    def __init__(self, game, x, y, image):
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False

        self.game.screen.blit(self.image, self.rect)
        return action


class ActionButton(Button):
    def __init__(self, game, x, y, text, tile_size):
        img = pygame.Surface((SIDE // 3, tile_size * 2 // 3))
        img.fill(BLACK)
        img_rect = img.get_rect()
        pygame.draw.rect(img, WHITE, (5, 5, img_rect.width - 10, img_rect.height - 10))
        draw_text(img, text, SIDE // 20, RED, img_rect.width // 2, img_rect.height // 2, 'center')
        Button.__init__(self, game, x, y, img)


class LetterButton(Button):
    def __init__(self, game, x, y, image):
        Button.__init__(self, game, x, y, image)
        self.color = WHITE
