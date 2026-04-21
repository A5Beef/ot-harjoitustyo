import unittest
from board import Board
from tetrominoes import Tetromino, TetrominoType


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_height(self):
        self.assertEqual(len(self.board.grid), 20)

    def test_board_width(self):
        self.assertEqual(len(self.board.grid[0]), 10)

    def test_invalid_position_x(self):
        OPiece = Tetromino(TetrominoType.O, x=-1, y=0)
        self.assertFalse(self.board._is_valid_position(OPiece))

    def test_valid_position(self):
        Lpiece = Tetromino(TetrominoType.L, x=0, y=0)
        self.assertTrue(self.board._is_valid_position(Lpiece))

    def test_invalid_position_y(self):
        Zpiece = Tetromino(TetrominoType.Z, x=0, y=23)
        self.assertFalse(self.board._is_valid_position(Zpiece))


class TestMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_rotate(self):
        self.board.rotate()
        self.assertEqual(self.board.currentblock.rotation, 1)

        self.board.rotate()
        self.assertEqual(self.board.currentblock.rotation, 2)

        self.board.rotate()
        self.assertEqual(self.board.currentblock.rotation, 3)

        self.board.rotate()
        self.assertEqual(self.board.currentblock.rotation, 0)

    def test_move_left(self):
        self.board.move_left()
        # block is in the middle so x value varies depending on block
        self.assertEqual(self.board.currentblock.x, 2)

    def test_move_right(self):
        self.board.move_right()
        self.assertEqual(self.board.currentblock.x, 4)  # same here

    def test_move_down(self):
        self.board.move_down()
        self.assertEqual(self.board.currentblock.y, 1)
        self.board.move_down()
        self.assertEqual(self.board.currentblock.y, 2)
