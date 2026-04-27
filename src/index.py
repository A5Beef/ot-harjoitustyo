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
MOVE_DELAY = 10
DAS = 10        # delay before auto-shift, kuinka kauan pitää painaa ennenkuin alkaa nopea liike
# auto-repeat rate, kuinka nopeasti palikka liikkuu DAS jälkeen
# 0 = heti, 1 = joka frame, 2 = joka toinen frame jne.
ARR = 3
LOCK_DELAY_MAX = 30

gravity_counter = 0
move_delay = 0
lock_delay = 0


running = True
while running:
    clock.tick(FPS)
    gravity_counter += 1

    # KEYDOWN vain rotate ja hard drop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                board.rotate()
            elif event.key == pygame.K_z:
                board.unrotate()
            elif event.key == pygame.K_SPACE:
                board.hard_drop()
                lock_delay = LOCK_DELAY_MAX  # ohittaa lock delay:n
            elif event.key == pygame.K_LSHIFT:
                board.hold_piece()

    # DAS liike
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]:
        move_delay += 1
        if move_delay == 1:  # ensimmäinen frame
            if keys[pygame.K_LEFT]:
                board.move_left()
            if keys[pygame.K_RIGHT]:
                board.move_right()
            if keys[pygame.K_DOWN]:
                board.move_down()
        elif move_delay >= DAS and (move_delay - DAS) % ARR == 0:
            if keys[pygame.K_LEFT]:
                board.move_left()
            if keys[pygame.K_RIGHT]:
                board.move_right()
            if keys[pygame.K_DOWN]:
                board.move_down()
    else:
        move_delay = 0

    # palat tippuu
    if gravity_counter >= GRAVITY_TICK:
        board.move_down()
        gravity_counter = 0

    # apu lukitsemiseen, alkaa laskemaan kun palikka on maassa, jos liikkuu tai rotatoi niin nollaa
    if board.is_on_ground:
        lock_delay += 1
        if lock_delay >= LOCK_DELAY_MAX:
            board.try_lock()
            lock_delay = 0
    else:
        lock_delay = 0

    renderer.render()

    # Tarkistaa onko peli ohi
    if board.gameover:
        print(f"Game Over! Final Score: {board.score}")
        running = False

pygame.quit()
