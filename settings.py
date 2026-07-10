# game options/settings
TITLE = "Wordle"
HEIGHT = 760
WIDTH = HEIGHT * 14 // 19
SIDE = min(WIDTH, HEIGHT)  # use for measurements based on smaller side of window
BORDER = 10
LETTER_BUTTON_SIZE = (WIDTH - BORDER * 11) // 10
FPS = 60

# define fonts
FONT_NAME = 'Arial'

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BG_COLOR_1 = BLUE
BG_COLOR_2 = WHITE
