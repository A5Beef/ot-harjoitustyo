import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_oikea_maara_rahaa_alussa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
        
    def test_oikea_maara_edullisia_alussa(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
     
    def test_oikea_maara_maukkaita_alussa(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kassan_rahamaara_kasvaa_vaihtoraha_oikein_edullisesti(self):
        self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)

    def test_kassan_rahamaara_kasvaa_vaihtoraha_oikein_maukkaasti(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)

    def test_lounasmaara_kasvaa_jos_maksu_edullisesti(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_lounasmaara_kasvaa_jos_maksu_maukkaasti(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_ei_riita_raha_kassa_pysyy_edullisesti(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_ei_riita_raha_kassa_pyysyy_maukkaasti(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_rahat_takas_jos_maksu_ei_riita(self):
        vaihtorahat = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(vaihtorahat, 200)

    def test_rahat_takas_jos_maksu_ei_riita_maukas(self):
        vaihtorahat = self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(vaihtorahat, 200)

    def test_lounaat_ei_muutosta(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_lounaat_ei_muutosta_maukas(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.maukkaat, 0)


class TestKassapaateKortti(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(500)

    def test_veloitus_toimii(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2.6)

    def test_veloitus_toimii_maukas(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 1.0)
        
    def test_palautetaan_true(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))

    def test_palautetaan_true_maukas(self):
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))

    def test_lounasmaara_kasvaa_jos_maksu_kortilla_edullisesti(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_lounasmaara_kasvaa_jos_maksu_kortilla_maukkaasti(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1) 



    def test_ei_riita_raha_pysyy_edullisesti_kortilla(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2.0)

    def test_ei_riita_raha_pyysyy_maukkaasti_kortilla(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2.0)

    def test_lounaat_ei_muutosta(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_lounaat_ei_muutosta_maukas(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_palautetaan_false(self):
        self.maksukortti = Maksukortti(200)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti))

    def test_palautetaan_false_maukas(self):
        self.maksukortti = Maksukortti(200)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti))



    def test_kassa_ei_muutu_kortilla(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_kassa_ei_muutu_kortilla_edullisesti(self):
        self.maksukortti = Maksukortti(200)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_kassa_ei_muutu_kortilla_on_rahaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_kassa_ei_muutu_kortilla_edullisesti_on_rahaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)
    

    def test_lataus_kasvattaa_kortin_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_lataus_kasvattaa_kassaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005.0)

    def test_negatiivinen_lataus_ei_muuta_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

    def test_negatiivinen_lataus_ei_muuta_kassaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)