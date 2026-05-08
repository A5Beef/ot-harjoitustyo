import pygame
from game.board import Board
from game.game_state import GameState
from game.config import (
    CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    FPS, GRAVITY_TICK, DAS, ARR, LOCK_DELAY_MAX, WINDOW_TITLE, BACKGROUND_COLOR
)
from graphics.menu import Menu
from graphics.renderer import Renderer



class Game:
    """Tetris-pelin päälogiikka ja ohjaus"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        self.state = GameState.MENU
        self.menu = Menu(self.screen)

        self.board = Board()
        self.renderer = Renderer(self.screen, self.board, CELL_SIZE)
        self.clock = pygame.time.Clock()

        # Pelin tilat
        self.running = True
        self.gravity_counter = 0
        self.move_delay = 0
        self.lock_delay = 0
        self.pause_selected = 0
        self.game_over_selected = 0

    def handle_input(self):
        """Käsittelee käyttäjän syötteet (painetut näppäimet ja sulkeminen)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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
            self.lock_delay = LOCK_DELAY_MAX
        elif event.key == pygame.K_LSHIFT:
            self.board.hold_piece()
        elif event.key == pygame.K_ESCAPE:
            self.state = GameState.PAUSED
            

    def _handle_continuous_movement(self, keys):
        """Käsittelee jatkuvat liikkeet (vasemmalle, oikealle, alas)"""
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]:
            self.move_delay += 1
            if self.move_delay == 1:
                self._move_piece(keys)
            elif self.move_delay >= DAS and (self.move_delay - DAS) % ARR == 0:
                self._move_piece(keys)
        else:
            self.move_delay = 0

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
        self.gravity_counter += 1
        if self.gravity_counter >= GRAVITY_TICK:
            self.board.move_down()
            self.gravity_counter = 0

    def handle_lock(self):
        """Hallitsee palikan lukitsemista pohjaan"""
        if self.board.is_on_ground:
            self.lock_delay += 1
            if self.lock_delay >= LOCK_DELAY_MAX:
                self.board.try_lock()
                self.lock_delay = 0
        else:
            self.lock_delay = 0

    def check_game_over(self):
        """Tarkistaa onko peli ohi ja tulostaa lopputuloksen"""
        if self.board.gameover:
            self.game_over_selected = 0
            self.state = GameState.GAME_OVER

    def _restart_game(self):
        """Aloittaa pelin alusta."""
        self.board = Board()
        self.renderer.board = self.board
        self.gravity_counter = 0
        self.move_delay = 0
        self.lock_delay = 0
        self.pause_selected = 0
        self.game_over_selected = 0
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
        while self.running:
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
                self.running = False
            else:
                choice = self.menu.handle_event(event)
                if choice == "Start Game":
                    self.state = GameState.PLAYING
                elif choice == "Exit":
                    self.running = False
        self.menu.draw()

    def _run_paused(self):
        """Hallitsee pelin taukotilaa"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_UP:
                    self.pause_selected = (self.pause_selected - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.pause_selected = (self.pause_selected + 1) % 3
                elif event.key == pygame.K_SPACE:
                    if self.pause_selected == 0:
                        self.state = GameState.PLAYING
                    elif self.pause_selected == 1:
                        self.state = GameState.MENU
                    elif self.pause_selected == 2:
                        self.running = False
        self.renderer.draw_choice_screen("PAUSED", ["Resume", "Main Menu", "Exit"], self.pause_selected)

    def _run_game_over(self):
        """Hallitsee game over -tilaa"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.game_over_selected = (self.game_over_selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    self.game_over_selected = (self.game_over_selected + 1) % 2
                elif event.key == pygame.K_SPACE:
                    if self.game_over_selected == 0:
                        self._restart_game()
                    elif self.game_over_selected == 1:
                        self.running = False
        self.renderer.draw_choice_screen("GAME OVER", ["Restart", "Exit"], self.game_over_selected)

def main():
    """Pääohjelma"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
