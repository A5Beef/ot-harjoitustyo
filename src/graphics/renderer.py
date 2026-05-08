import pygame
from game.config import FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT


class Renderer:
    """Hallinnoi pelin grafiikan renderoimista Pygamella.
    
    Piirtää peliruudukon, palikat, seuraavan palikan, hold-palikan ja pelin käyttöliittymän.
    """
    def __init__(self, screen, board, cell_size):
        self.screen = screen
        self.board = board
        self.cell_size = cell_size
        self._overlay_surface = None

    def render(self):
        """Piirtää koko pelin näytön.
        
        Tyhjentää ruudun, piirtää kaikki pelikomponentit ja päivittää näytön.
        """
        self._render_internal()
        pygame.display.flip()

    def _render_internal(self):
        """Sisäinen renderointikelpoinen - piirtää ilman display.flip() kutsua."""
        self.screen.fill((0, 0, 0))  # musta tausta, toistaiseksi
        self._draw_board()
        self._draw_current_piece()
        self._draw_next_piece()
        self._draw_hold_piece()
        self._draw_ui()

    def _draw_board(self):
        """Piirtää paikallaan olevat palikat ruudukolla.
        
        Käy läpi peliruudukon ja piirtää värityt ruudut sekä ruudukkorivit.
        """
        for row in range(20):
            for col in range(10):
                cell_rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                color = self.board.grid[row][col]
                if color is not None:
                    pygame.draw.rect(self.screen, color, cell_rect)

                # ruudukkoviivat piirretään aina, jotta koko pelilauta näkyy ruutuna
                pygame.draw.rect(self.screen, (50, 50, 50), cell_rect, 1)

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

    def _get_overlay_surface(self):
        if self._overlay_surface is None:
            self._overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self._overlay_surface.set_alpha(150)
            self._overlay_surface.fill((0, 0, 0))
        return self._overlay_surface

    def draw_choice_screen(self, title, options, selected_index, title_position=(100, 100), option_position=(110, 250)):
        """Piirtää valintaruudun pelin päälle."""
        self._render_internal()

        self.screen.blit(self._get_overlay_surface(), (0, 0))

        font_title = pygame.font.Font(FONT_PATH, 40)
        font_options = pygame.font.Font(FONT_PATH, 28)

        self.screen.blit(font_title.render(title, True, (255, 255, 255)), title_position)
        for index, option in enumerate(options):
            color = (255, 255, 0) if index == selected_index else (255, 255, 255)
            text_surface = font_options.render(option, True, color)
            self.screen.blit(text_surface, (option_position[0], option_position[1] + index * 60))

        pygame.display.flip()

