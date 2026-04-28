import pygame
from game.config import FONT_PATH


class Renderer:
    """Hallinnoi pelin grafiikan renderoimista Pygamella.
    
    Piirtää peliruudukon, palikat, seuraavan palikan, hold-palikan ja pelin käyttöliittymän.
    """
    def __init__(self, screen, board, cell_size):
        self.screen = screen
        self.board = board
        self.cell_size = cell_size

    def render(self):
        """Piirtää koko pelin näytön.
        
        Tyhjentää ruudun, piirtää kaikki pelikomponentit ja päivittää näytön.
        """
        self.screen.fill((0, 0, 0))  # musta tausta, toistaiseksi
        self._draw_board()
        self._draw_current_piece()
        self._draw_next_piece()
        self._draw_hold_piece()
        self._draw_ui()
        pygame.display.flip()

    def _draw_board(self):
        """Piirtää paikallaan olevat palikat ruudukolla.
        
        Käy läpi peliruudukon ja piirtää värityt ruudut sekä ruudukkorivit.
        """
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
        """Piirtää nykyisen palikan ja sen varjo-palikan.
        
        Piirtää ensin varjo-palikan harmaalla, sitten nykyisen palikan sen oikealla värillä.
        """
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
                # ruudukkoviivan piirtäminen tippuva palikka
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    (x * self.cell_size, y * self.cell_size,
                     self.cell_size, self.cell_size),
                    1
                )

    def _draw_next_piece(self):
        """Piirtää seuraavan palikan oikeassa yläkulmassa.
        
        Näyttää pelaajalle mikä palikka tulee seuraavaksi.
        """
        if self.board.nextblock:
            # piirtää seuraavan palikan oikeaan yläkulmaan
            blocks = self.board.nextblock.get_blocks()
            min_x = min(x for x, y in blocks)
            min_y = min(y for x, y in blocks)
            piece_w = (max(x for x, y in blocks) - min_x + 1) * self.cell_size
            piece_h = (max(y for x, y in blocks) - min_y + 1) * self.cell_size

            # lasketaan offsetit, jotta palikka on keskitettynä kehykseen
            ox = 308 + 175 // 2 - piece_w // 2 - min_x * self.cell_size
            oy = 108 + 200 // 2 - piece_h // 2 - min_y * self.cell_size

            for x, y in blocks:
                r = (ox + x * self.cell_size, oy + y *
                     self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.board.nextblock.color, r)
                pygame.draw.rect(self.screen, (100, 100, 100), r, 1)

    def _draw_hold_piece(self):
        """Piirtää hold-palikan oikeassa alakulmassa.
        
        Näyttää pelaajalle mikä palikka on pois lyöty hold-toiminnolla.
        """
        if self.board.holdblock:
            # piirtää hold palikan oikealle
            blocks = self.board.holdblock.get_blocks()
            min_x = min(x for x, y in blocks)
            min_y = min(y for x, y in blocks)
            piece_w = (max(x for x, y in blocks) - min_x + 1) * self.cell_size
            piece_h = (max(y for x, y in blocks) - min_y + 1) * self.cell_size

            # lasketaan offsetit, jotta palikka on keskitettynä kehykseen
            ox = 308 + 175 // 2 - piece_w // 2 - min_x * self.cell_size
            oy = 278 + 200 // 2 - piece_h // 2 - min_y * self.cell_size

            for x, y in blocks:
                r = (ox + x * self.cell_size, oy + y *
                     self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.board.holdblock.color, r)
                pygame.draw.rect(self.screen, (100, 100, 100), r, 1)

    def _draw_ui(self):
        """Piirtää pelin käyttöliittymä - pisteet ja tekstitiedot.
        
        Piirtää pisteet, "NEXT" ja "HOLD" -kehykset sekä näiden ympärillä olevat rajaukset.
        """
        big_font = pygame.font.Font(FONT_PATH, 22)
        # pisteytys teksti
        score_text = big_font.render("SCORE:", True, (255, 255, 255))
        score_value = big_font.render(
            str(self.board.score), True, (255, 255, 255))
        self.screen.blit(score_text, (320, 20))
        self.screen.blit(score_value, (320, 55))

        # seuraava palikka teksti ja suorakulmio
        smaller_font = pygame.font.Font(FONT_PATH, 16)
        self.screen.blit(smaller_font.render(
            "NEXT",  True, (180, 180, 180)), (320, 120))
        self.screen.blit(smaller_font.render(
            "PIECE", True, (180, 180, 180)), (390, 140))
        pygame.draw.rect(self.screen, (255, 255, 255), (308, 108, 175, 160), 2)

        # hold teksti ja suorakulmio ympärillä
        self.screen.blit(smaller_font.render(
            "HOLD",  True, (180, 180, 180)), (320, 300))
        pygame.draw.rect(self.screen, (255, 255, 255), (308, 285, 175, 160), 2)
