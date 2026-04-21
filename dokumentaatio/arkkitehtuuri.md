# Tetris - Luokkakaavio

```mermaid
classDiagram
    class Board {
        -grid: list
        -currentblock: Tetromino
        -nextblock: Tetromino
        -score: int
        -gameover: bool
        +move_left()
        +move_right()
        +move_down()
        +rotate()
        +unrotate()
        -_is_valid_position(piece: Tetromino) bool
        -_lock_piece()
        -_clear_lines()
    }

    class Tetromino {
        -type: TetrominoType
        -x: int
        -y: int
        -rotation: int
        +get_blocks() list
        +rotate()
        +unrotate()
        +color: tuple
    }

    class TetrominoType {
        <<enumeration>>
        I
        O
        T
        S
        Z
        J
        L
    }

    class GameState {
        <<enumeration>>
        MENU
        PLAYING
        PAUSED
        GAME_OVER
    }

    class Renderer {
        -screen: pygame.Surface
        -board: Board
        -cell_size: int
        +render()
        -_draw_board()
        -_draw_current_piece()
        -_draw_ui()
    }

    Board "1" --> "1" Tetromino: currentblock
    Board "1" --> "1" Tetromino: nextblock
    Tetromino --> TetrominoType: type
    Renderer --> Board: uses
    Renderer --> pygame: renders with
```

## Luokkien kuvaukset

### Board
- Hallinnoi pelilautaa ja pelimekaniikkaa
- Säilyttää pelaajan pisteit' ja nykyisen palikoiden tilan
- Käsittelee palikan liikkeet (vasen, oikea, alas) ja rotaation

### Tetromino
- Säilyttää palikan tyypin, sijainnin ja rotaatiosuunnan
- Laskee palikan nykyiset ruudukon koordinaatit

### TetrominoType
- Numeroidut palikka tyypit
- I, O, T, S, Z, J, L

### Renderer
- Piirtää peliruudun ja visuaaliset elementit
- Käyttää Pygamea renderointiin

### GameState
- Numerot pelin eri tiloille
- Käytetään pelin tilanhallintaan

# Tetris - Sekvenssikaavio
Sovelluksen toimintologiikka sekvenssikaaviona.

Kun pelaaja painaa alanuolta ja palikka osuu pohjaan tai toiseen palikkaan, etenee logiikka alla olevan kaavion mukaisesti

```mermaid
sequenceDiagram
  actor Player
  participant index.py
  participant Board
  participant Tetromino

  Player->>index.py: alanuoli (K_DOWN) 
  index.py->>Board: move_down()
  Board->>Tetromino: get_blocks()
  Tetromino-->>Board: koordinaatit
  Board-->>index.py: False (ei voi liikkua)
  index.py->>index.py: lock_delay += 1

  loop is_on_ground
    index.py->>index.py: lock_delay += 1
  end

  index.py->>Board: try_lock()
  Board->>Board: _lock_piece()
  Board->>Tetromino: get_blocks()
  Tetromino-->>Board: koordinaatit
  Board->>Board: grid[y][x] = color
  Board->>Board: _clear_lines()
  Board-->>Board: score += pisteet
  Board->>Tetromino: Tetromino(nextblock.type)
  Board-->>index.py: True
```
move_down() palauttaa False, kun palikka ei enää pysty liikkumaan alaspäin ja asettaa is_on_ground-lipun todeksi.
Tämän jälkeen index.py alkaa kasvattaa lock_delay-laskuria joka framella. Kun laskuri saavuttaa maksimin (LOCK_DELAY_MAX), kutsutaan try_lock()-metodia.
Board lukitsee palikan kirjoittamalla sen värin ruudukkoon _lock_piece()-metodissa, minkä jälkeen kutsutaan _clear_lines(), joka poistaa täydet rivit ja lisää pisteet.
Lopuksi currentblock vaihdetaan aiemmin arvottuun nextblock-palikkaan ja arvotaan uusi tuleva palikka.
