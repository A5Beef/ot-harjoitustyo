import random
from .tetrominoes import Tetromino, TetrominoType

BOARD_WIDTH = 10
BOARD_HEIGHT = 20


class Board:
    def __init__(self):  # alustava, random palikat tyhjä kenttä
        self.grid = [[None]*10 for _ in range(20)]
        self.currentblock = Tetromino(random.choice(list(TetrominoType)))
        self.nextblock = Tetromino(random.choice(list(TetrominoType)))
        self.score = 0
        self.gameover = False

    def _is_valid_position(self, piece: Tetromino):  # tarkistaa tyhjä tai reunat
        for x, y in piece.get_blocks():
            if x < 0 or x >= 10:  # tarkistaa vasen ja oikean reunan
                return False
            if y >= 20:  # tarkistaa alareunan
                return False
            if self.grid[y][x] is not None:  # tarkistaa onko ruutu tyhjä
                return False
        return True  # tarkistetty, ok
