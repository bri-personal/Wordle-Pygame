from wordle.game import Game
from wordle.sprites import *

if __name__ == '__main__':
    g = Game()
    while g.running:
        g.new()

    pygame.quit()
