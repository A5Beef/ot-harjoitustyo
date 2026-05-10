from dataclasses import dataclass
import pygame
from game.board import Board
from game.game_state import GameState
from game.config import (
    CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    FPS, GRAVITY_TICK, DAS, ARR, LOCK_DELAY_MAX, WINDOW_TITLE, BACKGROUND_COLOR)
from graphics.menu import Menu
from graphics.renderer import Renderer

@dataclass
class GameRuntime:
    running: bool = True
    gravity_counter: int = 0
    move_delay: int = 0
    lock_delay: int = 0
    pause_selected: int = 0
    game_over_selected: int = 0

class Game:
    """Tetris-pelin päälogiikka ja ohjaus"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.state = GameState.MENU
        self.menu = Menu(self.screen)
        self.board = Board()
        self.renderer = Renderer(self.screen, self.board, CELL_SIZE)
        self.clock = pygame.time.Clock()

        self.runtime = GameRuntime()

    def handle_input(self):
        """Käsittelee käyttäjän syötteet (painetut näppäimet ja sulkeminen)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runtime.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

        # DAS liike (delayed auto-shift)
        keys = pygame.key.get_pressed()
        self._handle_continuous_movement(keys)

    def _handle_keydown(self, event):
        """Käsittelee yksittäiset näppäinpainallukset"""
        if event.key == pygame.K_x:
            self.board.rotate()
        elif event.key == pygame.K_z:
            self.board.unrotate()
        elif event.key == pygame.K_SPACE:
            self.board.hard_drop()
            self.runtime.lock_delay = LOCK_DELAY_MAX
        elif event.key == pygame.K_LSHIFT:
            self.board.hold_piece()
        elif event.key == pygame.K_ESCAPE:
            self.state = GameState.PAUSED

    def _handle_continuous_movement(self, keys):
        """Käsittelee jatkuvat liikkeet (vasemmalle, oikealle, alas)"""
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]:
            self.runtime.move_delay += 1
            if self.runtime.move_delay == 1:
                self._move_piece(keys)
            elif self.runtime.move_delay >= DAS and (self.runtime.move_delay - DAS) % ARR == 0:
                self._move_piece(keys)
        else:
            self.runtime.move_delay = 0

    def _move_piece(self, keys):
        """Siirtää palikkaa näppäimen pohjalta"""
        if keys[pygame.K_LEFT]:
            self.board.move_left()
        if keys[pygame.K_RIGHT]:
            self.board.move_right()
        if keys[pygame.K_DOWN]:
            self.board.move_down()

    def update_gravity(self):
        """Päivittää painovoiman - palikka putoaa alas"""
        self.runtime.gravity_counter += 1
        if self.runtime.gravity_counter >= GRAVITY_TICK:
            self.board.move_down()
            self.runtime.gravity_counter = 0

    def handle_lock(self):
        """Hallitsee palikan lukitsemista pohjaan"""
        if self.board.is_on_ground:
            self.runtime.lock_delay += 1
            if self.runtime.lock_delay >= LOCK_DELAY_MAX:
                self.board.try_lock()
                self.runtime.lock_delay = 0
        else:
            self.runtime.lock_delay = 0

    def check_game_over(self):
        """Tarkistaa onko peli ohi ja tulostaa lopputuloksen"""
        if self.board.gameover:
            self.runtime.game_over_selected = 0
            self.state = GameState.GAME_OVER

    def _restart_game(self):
        """Aloittaa pelin alusta."""
        self.board = Board()
        self.renderer.board = self.board
        self.runtime.gravity_counter = 0
        self.runtime.move_delay = 0
        self.runtime.lock_delay = 0
        self.runtime.pause_selected = 0
        self.runtime.game_over_selected = 0
        self.state = GameState.PLAYING

    def update(self):
        """Päivittää pelin tilaa (syötteet, painovoima, lukitsu, pelin loppuminen)"""
        self.handle_input()
        self.update_gravity()
        self.handle_lock()
        self.check_game_over()

    def render(self):
        """Piirtää näytön"""
        self.screen.fill(BACKGROUND_COLOR)
        self.renderer.render()

    def run(self):
        """Pelin päälooppi - hallitsee pelin tilaa ja päivitystä"""
        while self.runtime.running:
            self.clock.tick(FPS)

            if self.state == GameState.MENU:
                self._run_menu()
            elif self.state == GameState.PLAYING:
                self.update()
                self.render()
            elif self.state == GameState.PAUSED:
                self._run_paused()
            elif self.state == GameState.GAME_OVER:
                self._run_game_over()

        pygame.quit()

    def _run_menu(self):
        """Hallitsee päävalikon toimintaa"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runtime.running = False
            else:
                choice = self.menu.handle_event(event)
                if choice == "Start Game":
                    # varmistetaan että peli on alusta alkaen,
                    # jos Start Game valitaan menuun paluun jälkeen.
                    self._restart_game()
                    self.state = GameState.PLAYING
                elif choice == "Exit":
                    self.runtime.running = False
        self.menu.draw()

    def _handle_paused_keydown(self, key):
        """Käsittelee näppäinpainallukset pause-tilassa
        """
        if key == pygame.K_ESCAPE:
            self.state = GameState.PLAYING
        elif key == pygame.K_UP:
            self.runtime.pause_selected = (self.runtime.pause_selected - 1) % 3
        elif key == pygame.K_DOWN:
            self.runtime.pause_selected = (self.runtime.pause_selected + 1) % 3
        elif key == pygame.K_SPACE:
            self._activate_paused_choice()

    def _activate_paused_choice(self):
        """Aktivoi valinnan pause-valikossa
        """
        if self.runtime.pause_selected == 0:
            self.state = GameState.PLAYING
        elif self.runtime.pause_selected == 1:
            self.state = GameState.MENU
        elif self.runtime.pause_selected == 2:
            self.runtime.running = False

    def _run_paused(self):
        """Hallitsee pause-tilaa"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runtime.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_paused_keydown(event.key)
        self.renderer.draw_choice_screen(
            "PAUSED", ["Resume", "Main Menu", "Exit"], self.runtime.pause_selected)

    def _handle_game_over_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.runtime.running = False
        elif key == pygame.K_UP:
            self.runtime.game_over_selected = (self.runtime.game_over_selected - 1) % 2
        elif key == pygame.K_DOWN:
            self.runtime.game_over_selected = (self.runtime.game_over_selected + 1) % 2
        elif key == pygame.K_SPACE:
            self._activate_game_over_choice()

    def _activate_game_over_choice(self):
        if self.runtime.game_over_selected == 0:
            self._restart_game()
        elif self.runtime.game_over_selected == 1:
            self.runtime.running = False

    def _run_game_over(self):
        """Hallitsee game over -tilaa"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runtime.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_game_over_keydown(event.key)
        self.renderer.draw_choice_screen(
            "GAME OVER", ["Restart", "Exit"], self.runtime.game_over_selected)


def main():
    """Pääohjelma"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
