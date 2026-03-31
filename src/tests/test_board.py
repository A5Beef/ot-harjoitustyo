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
        OPiece = Tetromino(TetrominoType.O, x=-1, y =0)
        self.assertFalse(self.board._is_valid_position(OPiece))
    
    def test_valid_position(self):
        Lpiece = Tetromino(TetrominoType.L, x=0, y=0)
        self.assertTrue(self.board._is_valid_position(Lpiece))

    def test_invalid_position_y(self):
        Zpiece = Tetromino(TetrominoType.Z, x=0, y=23)
        self.assertFalse(self.board._is_valid_position(Zpiece))