import unittest
from unittest.mock import Mock, call
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

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_hinnan(self):
        tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "piima", 3),
        }
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: tuotteet.get(tuote_id)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        calls = self.pankki_mock.tilisiirto.call_args_list
        self.assertEqual(calls[0].args[-1], 5)
        self.assertEqual(calls[1].args[-1], 3)

    def test_tilimaksu_pyytää_jokaiselle_ostokselle_uuden_viitteen(self):
        tuote = Tuote(1, "maito", 5)
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: tuote if tuote_id == 1 else None

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_tuotteen_poisto_korista_palauttaa_tuotteen_varastoon(self):
        tuote = Tuote(1, "maito", 5)
        self.varasto_mock.saldo.return_value = 10
        self.varasto_mock.hae_tuote.return_value = tuote

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)

        self.varasto_mock.palauta_varastoon.assert_called_once_with(tuote)

    def test_perakkaisissa_maksuissa_pankille_annetaan_oikeat_kutsut(self):
        tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "piima", 3),
        }
        self.varasto_mock.saldo.side_effect = lambda tuote_id: 10
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: tuotteet.get(tuote_id)
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "1111")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("liisa", "2222")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("maija", "3333")

        self.assertEqual(
            self.pankki_mock.tilisiirto.call_args_list,
            [
                call("pekka", 1, "1111", "33333-44455", 5),
                call("liisa", 2, "2222", "33333-44455", 3),
                call("maija", 3, "3333", "33333-44455", 8),
            ],
        )
