# Copilotin käyttäjäkokemukset

## Koodin täydennykset

Koodin täydennys auttoi aika paljon etenkin silloin, kun piti kirjoittaa samaa toistuvaa koodia, kuten pelaajien filtteröintiä ja järjestelyä. Homma sujui nopeammin, mutta ehdotukset oli silti pakko tarkistaa tarkkaan ennen kuin niitä löi lukkoon. Esim. metodin toimivuus kannattaa aina varmistaa suoraan docstringistä eikä vaa luottaa siihen, että tekoälyn ehdotus on heti valmista tavaraa.

## Pylint-varoitus

Copilotin selitys piti paikkansa. `os`-moduulia ei käytetty, joten Pylint
antoi `unused-import`-varoituksen. Käyttämätön tuonti poistettiin.

## Agentti ja testit

Agentti teki toimivan testisetin PlayerStats-luokalle, koska testeissä käytettiin PlayerReaderStub-stubia, eli mitään turhia verkkopyyntöjä ei tehty. Testit tarkistavat, että pelaajien järjestäminen kansalaisuuden tai joukkueen mukaan toimii ja, että myös monessa joukkueessa olemiset huomioidaan oikein.

Ensimmäinen uv run pytest -yritys kaatui ensin siihen, ettei player-moduulia löytynyt, mutta agentti korjasi ongelman lisäämällä pythonpath = ["src"] -määrityksen pyproject.toml-tiedostoon. Sen jälkeen kaikki kolme testiä menivätkin kerralla läpi.

## Vertailu edellisen viikon testeihin

Testeissä mentiin samalla stub-idealla kuin viime viikon NHL-tehtävässä: oikean datanhakijan tilalla käytettiin omaa luokkaa, joka palautti suoraan ennalta sovitut pelaajat. Testit oli kirjoitettu unittest-tyyliin, vaikka ne ajettiinkin pytestillä. Erona oli lähinnä se, että nyt testejä oli enemmän ja niissä tarkistettiin erikseen pisteiden mukainen järjestys sekä ne tilanteet, joissa pelaaja edustaa useampaa jengiä.

## Pylintin havainnot agentin koodista

Pylint löysi agentin koodista yhden liian pitkän rivin, joka oli top_goal_scorers-metodin turhan pitkä docstring, kun rivin pätkäistiin, Pylintiltä tuli 10.00/10. 

## Mitä muuta opin?

Tuli opittua, että pienemmätkin refaktoroinnit kannattaa aina testata erikseen stubin kanssa, verkkopalveluista riippumattomat testit ovat nopeita ja luotettavia. Tajusin myös, että uv run pytest vaatii toimiakseen oikeat import-asetukset, eli pyproject toml-tiedostoon kannattaa määritellä suoraan Pythonin moduulihakupolku.

Lisäksi kokeilun kautta tuli selkeäksi se, että Copilotin ja agentin koodiin ei pidä täysin luottaa, vaikka ehdotus näyttäisi hyvältä, sen toimivuus, koodityyli, testattavuus ja Pylint-säännöt pitää aina käydä itse läpi.
