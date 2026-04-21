import pygame

class Renderer:
    def __init__(self, screen, board, cell_size):
        self.screen = screen
        self.board = board
        self.cell_size = cell_size

    def render(self):
        self.screen.fill((0, 0, 0))  # clear screen
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

                    # locked blocks draw
                    pygame.draw.rect(self.screen, (50, 50, 50),
                                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)

    def _draw_current_piece(self):
        if self.board.currentblock:
            #ghostpiece
            ghost = self.board.ghost_piece()
            for x, y in ghost.get_blocks():
                pygame.draw.rect(self.screen, (100, 100, 100), 
                (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
            
            #currentpiece
            for x, y in self.board.currentblock.get_blocks():
                pygame.draw.rect(
                    self.screen,
                    self.board.currentblock.color,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                )
                # gridlines
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    1
                )

    def _draw_ui(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.board.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (320, 20))
