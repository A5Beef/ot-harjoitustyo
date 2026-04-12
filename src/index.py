import os  # pylint: disable=unused-import
import pygame  # pylint: disable=unused-import
# work in progress

pygame.init()
screen = pygame.display.set_mode((500, 600))

screen.fill((0, 0, 0))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
