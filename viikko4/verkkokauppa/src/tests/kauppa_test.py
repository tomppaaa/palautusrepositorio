import unittest
from unittest.mock import Mock
from kauppa import Kauppa
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()
        self.kauppa = Kauppa(
            self.varasto_mock,
            self.pankki_mock,
            self.viitegeneraattori_mock,
        )

    def test_ostos_varastossa_oleva_tuote_ja_loppunut_tuote(self):
        tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "loppunut", 3),
        }
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10 if tuote_id == 1 else 0
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: tuotteet.get(tuote_id)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_ostos_kaksi_samaa_tuotetta_oikeilla_parametreilla(self):
        tuote = Tuote(1, "maito", 5)
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10 if tuote_id == 1 else 0
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: tuote if tuote_id == 1 else None

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 10
        )

    def test_ostos_kahdella_tuotteella_oikeilla_parametreilla(self):
        tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "piima", 3),
        }
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10 if tuote_id in tuotteet else 0
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: tuotteet.get(tuote_id)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 8
        )

    def test_ostos_tilisiirto_oikeilla_parametreilla(self):
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10 if tuote_id == 1 else 0
        self.varasto_mock.hae_tuote.side_effect = (
            lambda tuote_id: Tuote(1, "maito", 5) if tuote_id == 1 else None
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista
