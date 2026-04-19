import random
from tetrominoes import Tetromino, TetrominoType

BOARD_WIDTH = 10
BOARD_HEIGHT = 20


class Board:
    def __init__(self):  # alustava, random palikat tyhjä kenttä
        self.grid = [[None]*10 for _ in range(20)]
        self.currentblock = Tetromino(random.choice(list(TetrominoType)))
        self.nextblock = Tetromino(random.choice(list(TetrominoType)))
        self.score = 0
        self.gameover = False
        self.is_on_ground = False

    def _is_valid_position(self, piece: Tetromino):  # tarkistaa tyhjä tai reunat
        for x, y in piece.get_blocks():
            if x < 0 or x >= 10:  # tarkistaa vasen ja oikean reunan
                return False
            if y >= 20:  # tarkistaa alareunan
                return False
            if self.grid[y][x] is not None:  # tarkistaa onko ruutu tyhjä
                return False
        return True  # tarkistetty, ok

    def move_left(self):
        self.currentblock.x -= 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.x += 1
        self._check_on_ground()

    def move_right(self):
        self.currentblock.x += 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.x -= 1
        self._check_on_ground()

    def move_down(self):
        self.currentblock.y += 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.y -= 1
            self.is_on_ground = True
            return False
        self.is_on_ground = False
        return True
    
    def hard_drop(self):
        while self.move_down():
            pass

    def _lock_piece(self): #lukitsee palat ja tarkistaa loppuiko peli
        for x, y in self.currentblock.get_blocks():
            self.grid[y][x] = self.currentblock.color

        self._clear_lines()
        self.currentblock = self.nextblock
        self.nextblock = Tetromino(random.choice(list(TetrominoType)))

        if not self._is_valid_position(self.currentblock):
            self.gameover = True

    def rotate(self):
        self.currentblock._rotate()
        if not self._is_valid_position(self.currentblock):
            self.currentblock._unrotate()

    def unrotate(self):
        self.currentblock._unrotate()
        if not self._is_valid_position(self.currentblock):
            self.currentblock._rotate()

    def _clear_lines(self): #tarkistaa ja tyhjentää täydet rivit
        cleared_rows = []
        for row in range(20):
            if None not in self.grid[row]:
                cleared_rows.append(row)

        points = {1:100 , 2:300, 3:500, 4:800} #pisteet rivien mukaan, myöhemmin levels, spins, combot, hard/soft drop.
        self.score += points.get(len(cleared_rows), 0)  # lisää pisteet, jos ei rivejä niin 0 pistettä

        # täysrivien poisto
        for row in reversed(cleared_rows):
            del self.grid[row]

        # Uudet rivit ylös, vanhat alas
        for _ in range(len(cleared_rows)):
            self.grid.insert(0, [None] * 10)

    def _check_on_ground(self):
        self.currentblock.y += 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.y -= 1
            self.is_on_ground = True
        else:
            self.currentblock.y -= 1
            self.is_on_ground = False