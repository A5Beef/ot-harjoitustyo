from enum import Enum


class TetrominoType(Enum):
    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"


# Jokaisen palikan muodot, 4 rotaatiota
SHAPES = {
    TetrominoType.I: [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
    ],
    TetrominoType.O: [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    TetrominoType.T: [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    TetrominoType.S: [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    TetrominoType.Z: [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    TetrominoType.J: [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    TetrominoType.L: [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

COLORS = {
    TetrominoType.I: (110, 222, 201),
    TetrominoType.O: (222, 201, 110),
    TetrominoType.T: (201, 110, 222),
    TetrominoType.S: (131, 222, 110),
    TetrominoType.Z: (208, 47, 77),
    TetrominoType.J: (47, 77, 208),
    TetrominoType.L: (246, 144, 85),
}


class Tetromino:
    def __init__(self, tetromino_type: TetrominoType, x: int = 3, y: int = 0):
        self.type = tetromino_type
        self.x = x
        self.y = y
        self.rotation = 0

    def get_blocks(self):
        """Palauttaa palikoiden absoluuttiset ruudukkokoordinaatit."""
        shape = SHAPES[self.type][self.rotation]
        return [(self.x + bx, self.y + by) for bx, by in shape]

    def _rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def _unrotate(self):
        self.rotation = (self.rotation - 1) % 4

    @property
    def color(self):
        return COLORS[self.type]
