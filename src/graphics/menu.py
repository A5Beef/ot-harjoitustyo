import pygame
from game.config import FONT_PATH


class Menu:
    def __init__(self, screen):
        """Hallinnoi pelin päävalikon grafiikkaa ja syötteitä.

        Luo fontit otsikolle, tekijän nimelle ja valikkovaihtoehdoille.
        Tallentaa valikkovaihtoehdot listana.
        """
        self.screen = screen
        self.font_title = pygame.font.Font(FONT_PATH, 48)
        self.font_creator = pygame.font.Font(FONT_PATH, 20)
        self.font_items = pygame.font.Font(FONT_PATH, 28)
        self.options = ["Start Game", "Exit"]
        self.selected = 0  # mikä vaihtoehto valittuna

    def draw(self):
        """Piirtää päävalikon näytölle

        Piirtää otsikon, tekijän nimen ja valikkovaihtoehdot.
        Valittu vaihtoehto korostetaan.
        """
        self.screen.fill((0, 0, 0))
        # title and creator text
        title = self.font_title.render("TETRIS", True, (255, 255, 255))
        creatortext = self.font_creator.render(
            "By A5Beef", True, (255, 255, 255))
        self.screen.blit(title, (50, 50))
        self.screen.blit(creatortext, (270, 100))

        # valinnat
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font_items.render(option, True, color)
            self.screen.blit(text, (110, 250 + i * 60))
        pygame.display.flip()

    def handle_event(self, event):
        """Käsittelee päävalikon syötteet
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_SPACE:
                return self.options[self.selected]
        return None
