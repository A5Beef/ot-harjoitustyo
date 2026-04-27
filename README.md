# Ohjelmistotekniikka, harjoitustyö - Tetris

Oma versioni Tetris-pelistä, pygamella tehty.
Tetris palikoihin on valittu minulle mieluisat värit :\)

## [Uusin release](https://github.com/A5Beef/ot-harjoitustyo/releases/tag/viikko5)

## Dokumentaatio


- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

## Asennus

1. Asenna riippuvuudet:

```bash
poetry install
```

2. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Muut komentorivitoiminnot

### Testaus

Testit voi suorittaa seuraavalla komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti avautuu automaattisesti selaimeen. Muuten sen löytää htmlcov kansiosta index.html tiedostona.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```

## Resurssit
- [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) -fontti: CodeMan38, [SIL Open Font License](https://scripts.sil.org/OFL)
