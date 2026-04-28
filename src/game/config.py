"""
Pelin konfiguraatiot ja vakiot
"""

import os

# Ruutu ja pelilauta
CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SCREEN_WIDTH = BOARD_WIDTH * CELL_SIZE + 200
SCREEN_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Peliaika ja syötteet
FPS = 60
GRAVITY_TICK = 30           # kuinka monen framen välein pala putoaa
DAS = 10                    # delay before auto-shift
                            #eli kuinka kauan pitää painaa ennenkuin alkaa nopea liike
ARR = 3                     # auto-repeat rate, kuinka nopeasti palikka liikkuu DAS jälkeen
LOCK_DELAY_MAX = 30         # kuinka kauan palikka voi pyöriä/liikkua ennen kuin lukitaan

# Fontti
FONT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "assets",
    "fonts",
    "PressStart2P-regular",
    "PressStart2P-Regular.ttf"
)

# Pelin ikkuna
WINDOW_TITLE = "Tetris"
BACKGROUND_COLOR = (0, 0, 0)
