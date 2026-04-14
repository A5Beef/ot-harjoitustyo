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
