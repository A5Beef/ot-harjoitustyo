import random
from .tetrominoes import Tetromino, TetrominoType


class Board:
    """Hallinnoi Tetris-pelilautaa ja pelimekaniikkaa.
    
    Säilyttää peliruudukon, nykyisen ja seuraavan palikan, pisteet ja pelin tilan.
    Käsittelee palikan liikkeet, rotaatiot, lukitsemisen ja rivien poistamisen.
    """
    def __init__(self):
        self.grid = [[None]*10 for _ in range(20)]
        self.currentblock = Tetromino(random.choice(list(TetrominoType)))
        self.nextblock = Tetromino(random.choice(list(TetrominoType)))
        self.holdblock = None
        self.heldblock = False
        self.score = 0
        self.gameover = False
        self.is_on_ground = False

    def _is_valid_position(self, piece: Tetromino):
        """Tarkistaa onko palikan uusi positio kelvollinen.
        
        Tarkistaa ettei palikka ole reunojen ulkopuolella tai muiden palikan päällä.
        
        Args:
            piece: Tetromino-objekti, jonka positiota tarkistetaan
            
        Returns:
            bool: True jos positio on kelvollinen, False muuten
        """
        for x, y in piece.get_blocks():
            if x < 0 or x >= 10:  # tarkistaa vasen ja oikean reunan
                return False
            if y >= 20:  # tarkistaa alareunan
                return False
            if self.grid[y][x] is not None:  # tarkistaa onko ruutu tyhjä
                return False
        return True  # tarkistettu, ok

    def move_left(self):
        """Siirtää nykyistä palikkaa vasemmalle.
        
        Jos uusi positio on kelvollinen, palikka siirretään. Muuten palikka pysyy paikallaan.
        """
        self.currentblock.x -= 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.x += 1
        self._check_on_ground()

    def move_right(self):
        """Siirtää nykyistä palikkaa oikealle.
        
        Jos uusi positio on kelvollinen, palikka siirretään. Muuten palikka pysyy paikallaan.
        """
        self.currentblock.x += 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.x -= 1
        self._check_on_ground()

    def move_down(self):
        """Siirtää nykyistä palikkaa alas.
        
        Jos palikka osuu pohjaan tai toiseen palikkaan, se lukitaan ja tilaksi
        asetetaan True.
        
        Returns:
            bool: True jos palikka siirtyi, False jos palikka osui pohjaan
        """
        self.currentblock.y += 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.y -= 1
            self.is_on_ground = True
            return False
        self.is_on_ground = False
        return True

    def hard_drop(self):
        """Pudottaa nykyisen palikan suoraan pohjaan.
        
        Kutsuu move_down() toistuvasti kunnes palikka osuu pohjaan tai toiseen palikkaan.
        """
        while self.move_down():
            pass

    def _lock_piece(self):
        """Lukitsee nykyisen palikan lautaan ja generoi seuraavan palikan.
        
        Sijoittaa nykyisen palikan ruudukkoihin, tyhjentää täydet rivit,
        kutsuu seuraavan palikan nykyiseksi ja generoi uuden seuraavan palikan.
        Jos uusi palikka ei mahdu, peli päättyy.
        """
        for x, y in self.currentblock.get_blocks():
            self.grid[y][x] = self.currentblock.color

        self._clear_lines()
        self.currentblock = self.nextblock
        self.nextblock = Tetromino(random.choice(list(TetrominoType)))
        self.heldblock = False  # resettaa holdin, voi käyttää taas

        if not self._is_valid_position(self.currentblock):
            self.gameover = True

    def try_lock(self):
        """Yrittää lukita palikan jos se on pohjassa.
        
        Returns:
            bool: True jos palikka lukitiin, False muuten
        """
        if self.is_on_ground:
            self._lock_piece()
            return True
        return False

    def rotate(self):
        """Pyörittää nykyistä palikkaa myötäpäivään.
        
        Käyttää wall-kick -mekanikka jos palikka osuu seinään rotaation jälkeen.
        Yrittää siirtää palikkaa oikealle tai vasemmalle rotaation jälkeen.
        """
        self.currentblock.rotate()

        if not self._is_valid_position(self.currentblock):
            # testataan pala oikealla
            self.currentblock.x += 1

            # testataan vasemmalla
            if not self._is_valid_position(self.currentblock):
                self.currentblock.x -= 2

                # ei mahdu, perutaan
                if not self._is_valid_position(self.currentblock):
                    self.currentblock.x += 1
                    self.currentblock.unrotate()

        self._check_on_ground()

    def unrotate(self):
        """Pyörittää nykyistä palikkaa vastapäivään.
        
        Käyttää wall-kick -mekanikka jos palikka osuu seinään rotaation jälkeen.
        Yrittää siirtää palikkaa oikealle tai vasemmalle rotaation jälkeen.
        """
        self.currentblock.unrotate()
        if not self._is_valid_position(self.currentblock):
            # testataan pala oikealla
            self.currentblock.x += 1

            # testataan vasemmalla
            if not self._is_valid_position(self.currentblock):
                self.currentblock.x -= 2

                # ei mahdu, perutaan
                if not self._is_valid_position(self.currentblock):
                    self.currentblock.x += 1
                    self.currentblock.rotate()

        self._check_on_ground()

    def _clear_lines(self):
        """Tarkistaa ja poistaa täydet rivit sekä lisää pisteet.
        
        Etsii kaikki täydet rivit, lisää vastaavat pisteet, poistaa täydet rivit
        ja lisää uusia tyhjiä rivejä ylös.
        """
        cleared_rows = []
        for row in range(20):
            if None not in self.grid[row]:
                cleared_rows.append(row)

        # pisteet rivien mukaan, myöhemmin levels, spins, combot, hard/soft drop.
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        # lisää pisteet, jos ei rivejä niin 0 pistettä
        self.score += points.get(len(cleared_rows), 0)

        # täysrivien poisto
        for row in reversed(cleared_rows):
            del self.grid[row]

        # Uudet rivit ylös, vanhat alas
        for _ in range(len(cleared_rows)):
            self.grid.insert(0, [None] * 10)

    def _check_on_ground(self):
        """Tarkistaa onko nykyinen palikka pohjassa tai toisen palikan päällä.
        
        Apumetodi jota kutsutaan liikkeen ja rotaation jälkeen.
        Päivittää is_on_ground-tilaa.
        """
        self.currentblock.y += 1
        if not self._is_valid_position(self.currentblock):
            self.currentblock.y -= 1
            self.is_on_ground = True
        else:
            self.currentblock.y -= 1
            self.is_on_ground = False

    def ghost_piece(self):
        """Luo "varjo"-palikan joka näyttää mihin nykyinen palikka putoaa.
        
        Returns:
            Tetromino: Uusi Tetromino-objekti joka on sijoitettu mihin nykyinen palikka putoaa
        """
        ghostblock = Tetromino(self.currentblock.type,
                               self.currentblock.x, self.currentblock.y)
        ghostblock.rotation = self.currentblock.rotation
        while True:
            ghostblock.y += 1
            if not self._is_valid_position(ghostblock):
                ghostblock.y -= 1
                return ghostblock

    def hold_piece(self):
        """Vaihtaa nykyisen palikan hold-palikaksi tai päinvastoin.
        
        Jos palikka on jo pidetty tässä kierroksessa, ei tee mitään.
        Muuten vaihtaa nykyisen ja hold-palikan keskenään.
        """
        if self.heldblock:
            return

        if self.holdblock:  # jos edellinen holdi olemassa niin vaihda sen kanssa paikkaa
            buffer = self.currentblock
            self.currentblock = self.holdblock
            self.currentblock.x = 3
            self.currentblock.y = 0
            self.currentblock.rotation = 0
            self.holdblock = buffer
        else:  # tyhjä holdi
            self.holdblock = self.currentblock
            self.currentblock = self.nextblock
            self.nextblock = Tetromino(random.choice(list(TetrominoType)))

        # Muuttaa True jos painetaan, estää spammin edes takaisin hold piecella.
        self.heldblock = True
