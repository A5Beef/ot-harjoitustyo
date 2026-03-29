## Monopoli, alustava luokkakaavio

---
title: Monopoly Diagram
---
classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    NormaalitKadut * --> "1" Pelaaja
    Ruutu <|-- Aloitusruutu
    Ruutu <|-- Vankila
    Ruutu <|-- Sattumajayhteismaa
    Ruutu <|-- Asematjalaitokset
    Ruutu <|-- NormaalitKadut
    Sattuma ja yhteismaa <-- Kortti
    class Ruutu{
        +numero int
        +toiminto type

    }
    class Aloitusruutu{
        +numero 1
    }
    class Vankila{
        +numero 11
    }
        class Kortti{
        +toiminto type
    }
    class NormaalitKadut["Normaalit kadut"]{
        +talot int
        +hotelli bool
    }
    class Pelaaja{
        +id int
        +raha int
    }

    note for NormaalitKadut "Constraint: talot ∈ [1..4]"