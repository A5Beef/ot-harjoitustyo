# Testausdokumentti

Ohjelmaa on testattu sekä automatisoiduin yksikkö- ja integraatiotestein unittestilla sekä manuaalisesti tapahtunein järjestelmätason testein.

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

Sovelluslogiikasta vastaavaa Board-luokkaa testataan TestBoard-testiluokalla. Testit kattavat pelimekaniikan kuten palikan liikkumisen, rivien tyhjentämisen, pisteytysjärjestelmän sekä pelin päättymisen.

Palikan kierrossa tapahtuva mahdollinen wall kick- mekaniikkaa ei testattu monimutkaisuuden vuoksi.

Integraatiotestit testaavat Board- ja Tetromino-luokkien yhteistoimintaa, kuten palikan lukituksen ruudukkoon ja seuraavan palikan ilmestymisen.

### UI

Käyttöliittymää ei ole testattu automatisoidusti. Päävalikko, pause-valikko ja game over -ruutu on testattu manuaalisesti. Pygame-riippuvuus tekee automaattitestauksesta hankalaa.

### Testauskattavuus

Sovelluksen testauksen haarautumakattavuus on 86%
![](./kuvat/kattavuusraportti.png)

Testaamatta jäivät index.py:n Game-luokka pygame-riippuvuuden vuoksi sekä graphics/-kansion renderer ja menu.

## Järjestelmätestaus

Testattu fuksiläppärillä cubbli OS:llä, sekä Virtual Machine (cubbli) nettiselaimessa, että henkilökohtaisella windows-järjestelmällä.
Windowsissa todettu, että invoke komennot ei toimi. Invoke komennot toimivat windowsilla "pty=True" poistetaan riveiltä. 

### Asennus ja konfigurointi

Sovellus on asennettu ja testattu Linux- ja Windows-ympäristöissä. Asennus tapahtuu poetry install -komennolla käyttöohjeen mukaisesti.

### Toiminnallisuudet

Kaikki määrittelydokumentin toiminnallisuudet on testattu manuaalisesti, mukaan lukien palikan liikkuminen, rotaatio, hard drop, hold, rivien tyhjentyminen, pisteytys, pause-toiminto sekä pelin uudelleenkäynnistys.

## Sovellukseen jääneet laatuongelmat

Game-luokan game state -logiikkaa ei ole testattu automaattisesti pygame-riippuvuuden vuoksi. Logiikka olisi voitu eriyttää paremmin omaksi luokaksi jolloin testaaminen olisi ollut mahdollista.

Pelin wallkick mekaanikkaa ei testattu monimutkaisuuden vuoksi.

menu.py:n event handling -logiikka olisi pitänyt olla erillisessä tiedostossa testattavuuden parantamiseksi. Arkkitehtuurillinen virhe tässä.