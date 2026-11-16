Kokemuksia agentin käytöstä

Ohjetiedosto

Agentti teki Login-tehtävää varten .github/instructions/login.instructions.md-tiedoston, missä oli ohjeet projektia varten. Sitä piti vähän tiivistää ja fiksailla, jotta siinä näkyy selkeästi oikeat uv run -komennot, sovelluksen käynnistys, se että Robot-testit vaativat sovelluksen olevan päällä, sekä tieto siitä että validointi löytyy user_service-tiedostosta.

Testit ennen toteutusta

Testien kirjoittaminen ennen varsinaista toteutusta onnistui niin kuin pitikin. Ensin lisättiin testit salasanan kirjainrajoitukselle ja vahvistukselle. Kun testit ajettiin ennen koodimuutoksia, ne epäonnistuivat.

Tämän jälkeen molemmat toteutettiin ja salasanan minimipituus pidettiin ennallaan.

Ohjauksen määrä

Agenttia piti ohjata useammassa eri vaiheessa esim. koodin rikkomistehtävässä sille täytyi tarkentaa, että testit kirjoitetaan ensin ja varmistetaan, että ne epäonnistuu. Sen jälkeen piti vielä erikseen pyytää, että toinen story tehdään vasta kun ensimmäinen on valmis. Lopuksi agenttia pyydettiin rikkomaan toteutus kahdella eri tavalla, ajamaan testit kummankin jälkeen ja korjaamaan jäljet.

Tämä ei siis hoitunut yhdellä kehotteella, mutta testien tuloksista sai aina hyvin kiinni, mitä seuraavaksi pitää pyytää.

Tarkoituksellinen rikkominen

Koodia rikottiin kahdessa eri tilanteessa: kirjainvalidointi käännettiin väärinpäin, kymmenestä rekisteröitymistestistä kahdeksan epäonnistui. Sama homma kävi, kun salasanan vahvistuksen tarkistus otettiin pois, silloinkin 8 testiä epäonnistui.

Lopuksi rikkomiset korjattiin, ja kaikki login-sovelluksen Robot-testit menivät läpi.

Mitä opin?

Tehtävästä jäi käteen se, että hyväksymiskriteerit kannattaa muokata konkreettisiksi käyttöliittymätesteiksi jo ennen varsinaisen toiminnallisuuden koodaamista. Lisäksi koodin tahallinen rikkominen osoittautui hyväksi tavaksi varmistaa, että testit oikeasti toimivat.

Huomasin myös, että agentin generoima ohjetiedosto voi olla erittäin hyödyllinen väline. 