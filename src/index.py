import pygame
from board import Board
from renderer import Renderer

CELL_SIZE = 30
BOARD_WIDTH = 300
BOARD_HEIGHT = 600
SCREEN_WIDTH = BOARD_WIDTH + 200
SCREEN_HEIGHT = BOARD_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

board = Board()
renderer = Renderer(screen, board, CELL_SIZE)

clock = pygame.time.Clock()
FPS = 60
GRAVITY_TICK = 30

gravity_counter = 0

running = True
while running:
    clock.tick(FPS)
    gravity_counter += 1

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board.move_left()
            elif event.key == pygame.K_RIGHT:
                board.move_right()
            elif event.key == pygame.K_DOWN:
                board.move_down()
            elif event.key == pygame.K_UP:
                board.rotate()

    # palat tippuu
    if gravity_counter >= GRAVITY_TICK:
        board.move_down()
        gravity_counter = 0

    renderer.render()

    # Check gameover
    if board.gameover:
        print(f"Game Over! Final Score: {board.score}")
        running = False

pygame.quit()
