from game.tetrominoes import Tetromino, TetrominoType
from game.board import Board
import unittest
import sys
import os

# Lisää parent directory, jotta importit toimivat
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


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

    def test_invalid_position_occupied(self):
        # täytetään koko grid, jotta kaikki paikat on varattuja
        self.board.grid = [[(255, 255, 255) for _ in range(10)] for _ in range(20)]
        Spiece = Tetromino(TetrominoType.S, x=0, y=0)
        self.assertFalse(self.board._is_valid_position(Spiece))

    def test_game_over(self):
        # täytetään koko grid, jotta kaikki paikat on varattuja
        self.board.grid = [[(255, 255, 255)] * 10 for _ in range(20)]
        self.board.nextblock = Tetromino(TetrominoType.O, x=3, y=0)
        self.board._clear_lines = lambda: None  # ohitetaan clearlines
        self.board._lock_piece()
        self.assertTrue(self.board.gameover)

    def test_clear_lines(self):
        # täytetään rivi 19, jotta se on valmis poistettavaksi
        self.board.grid[19] = [(255, 255, 255)] * 10
        self.board._clear_lines()
        self.assertEqual(self.board.grid[19], [None] * 10)

    def test_check_not_on_ground(self):
        self.board.currentblock = Tetromino(TetrominoType.O, x=0, y=0) #ilmassa
        self.board._check_on_ground()
        self.assertFalse(self.board.is_on_ground)

    def test_check_on_ground_true(self):
        self.board.currentblock = Tetromino(TetrominoType.O, x=0, y=18)
        self.board._check_on_ground()
        self.assertTrue(self.board.is_on_ground)

    def test_check_ghost_piece(self):
        self.board.currentblock = Tetromino(TetrominoType.O, x=0, y=0)
        self.assertEqual(self.board.ghost_piece().y, 18) # varjo-palikka on pohjalla

        # Muut arvot (x, rotation, type) pitäisi olla samat kuin nykyisellä palikalla
        self.assertEqual(self.board.ghost_piece().x, self.board.currentblock.x)
        self.assertEqual(self.board.ghost_piece().rotation, self.board.currentblock.rotation)
        self.assertEqual(self.board.ghost_piece().type, self.board.currentblock.type)

        #testataan että ghostpiece päivittyy myös rotaation ja liikkeen jälkeen
        self.board.rotate()
        self.board.move_left()
        self.assertEqual(self.board.ghost_piece().x, self.board.currentblock.x)
        self.assertEqual(self.board.ghost_piece().rotation, self.board.currentblock.rotation)

    def test_holding_not_allowed_after_hold(self):
        self.board.currentblock = Tetromino(TetrominoType.O, x=0, y=0)
        self.board.nextblock = Tetromino(TetrominoType.I, x=4, y=0)
        self.board.hold_piece() # ensimmäinen hold
        self.assertEqual(self.board.holdblock.type, TetrominoType.O)
        self.assertEqual(self.board.currentblock.type, TetrominoType.I)

        self.board.hold_piece() # yrittää holdata uudestaan
        self.assertNotEqual(self.board.holdblock.type, self.board.currentblock.type)
        self.assertEqual(self.board.currentblock.type, TetrominoType.I)
        self.assertEqual(self.board.holdblock.type, TetrominoType.O)

    def test_scoring(self):
        self.assertEqual(self.board.score, 0) # alussa 0 pistettä
        # täytetään rivi 19
        self.board.grid[19] = [(255, 255, 255)] * 10
        self.board._clear_lines()
        self.assertEqual(self.board.score, 100) # yksi rivi = 100 pistettä


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

    def test_unrotate(self):
        self.board.unrotate()
        self.assertEqual(self.board.currentblock.rotation, 3)

    def test_move_left(self):
        self.board.move_left()
        # palikka on keskellä, joten x-arvo vaihtelee riippuen palikasta..
        self.assertEqual(self.board.currentblock.x, 2)

    def test_move_right(self):
        self.board.move_right()
        self.assertEqual(self.board.currentblock.x, 4)  # tässä sama

    def test_move_down(self):
        self.board.move_down()
        self.assertEqual(self.board.currentblock.y, 1)
        self.board.move_down()
        self.assertEqual(self.board.currentblock.y, 2)

    def test_hard_drop(self):
        self.board.hard_drop()
        self.assertTrue(self.board.is_on_ground)

    def test_move_right_blocked(self):
        self.board.currentblock = Tetromino(TetrominoType.I, x=5, y=0) #palikka on keskellä
        for _ in range (10): #varmistetaan että palikka on oikeassa reunassa
            self.board.move_right()
        self.assertEqual(self.board.currentblock.x, 6) #palikka ei voi mennä oikean reunan yli
    
    def test_move_left_blocked(self):
        self.board.currentblock = Tetromino(TetrominoType.I, x=5, y=0) #palikka on keskellä
        for _ in range (10): #varmistetaan että palikka on vasemmassa reunassa
            self.board.move_left()
        self.assertEqual(self.board.currentblock.x, 0) #palikka ei voi mennä vasemman reunan yli


class TestLockPiece(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.currentblock = Tetromino(TetrominoType.O, x=4, y=0)
        self.board.nextblock = Tetromino(TetrominoType.O, x=4, y=0)

    def test_lock_piece_changes_grid(self):
        block = self.board.currentblock
        self.board.hard_drop()
        self.board._lock_piece()

        for x, y in block.get_blocks():
            self.assertEqual(self.board.grid[y][x], block.color)

    def test_lock_piece_on_ground(self):
        self.board.hard_drop()
        self.assertTrue(self.board.is_on_ground)
        self.board.try_lock()
        self.assertTrue(self.board.grid[19][4] is not None) #palikka on lukittu pohjaan

    def test_lock_piece_not_on_ground(self):
        self.board.move_down() #palikka on vielä ilmassa
        self.board.try_lock()
        self.assertTrue(self.board.grid[19][4] is None) #palikka ei lukittu, koska ei pohjassa


class TestHoldPiece(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.currentblock = Tetromino(TetrominoType.O, x=4, y=0)
        self.board.nextblock = Tetromino(TetrominoType.I, x=4, y=0)

    def test_hold_piece(self):
        self.board.hold_piece()
        self.assertEqual(self.board.holdblock.type, TetrominoType.O)
        self.assertEqual(self.board.currentblock.type, TetrominoType.I)

        self.board.nextblock = Tetromino(TetrominoType.S, x=4, y=0) # asetetaan nextblock
        self.board._lock_piece() # lukitaan palikka, jotta uusi palikka tulee tilalle
        self.assertEqual(self.board.currentblock.type, TetrominoType.S)

        self.board.hold_piece() # vaihdetaan taas
        self.assertEqual(self.board.holdblock.type, TetrominoType.S)
        self.assertEqual(self.board.currentblock.type, TetrominoType.O) 
