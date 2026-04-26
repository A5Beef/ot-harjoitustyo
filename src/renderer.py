import pygame


class Renderer:
    def __init__(self, screen, board, cell_size):
        self.screen = screen
        self.board = board
        self.cell_size = cell_size

    def render(self):
        self.screen.fill((0, 0, 0))  # musta tausta, toistaiseksi
        self._draw_board()
        self._draw_current_piece()
        self._draw_ui()
        pygame.display.flip()

    def _draw_board(self):
        for row in range(20):
            for col in range(10):
                color = self.board.grid[row][col]
                if color is not None:
                    pygame.draw.rect(self.screen, color,
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

                    # ruudukkoviivan piirtäminen
                    pygame.draw.rect(self.screen, (50, 50, 50),
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)

    def _draw_current_piece(self):
        if self.board.currentblock:
            # ghost piece - eli varjo mihin palikka putoaisi
            ghost = self.board.ghost_piece()
            for x, y in ghost.get_blocks():
                pygame.draw.rect(self.screen, (100, 100, 100),
                (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

            # nykyinen palikan piirtäminen
            for x, y in self.board.currentblock.get_blocks():
                pygame.draw.rect(
                    self.screen,
                    self.board.currentblock.color,
                    (x * self.cell_size, y * self.cell_size,
                     self.cell_size, self.cell_size)
                )
                #ruudukkoviivan piirtäminen tippuva palikka
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    (x * self.cell_size, y * self.cell_size,
                     self.cell_size, self.cell_size),
                    1
                )

    def _draw_ui(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(
            f"Score: {self.board.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (320, 20))
