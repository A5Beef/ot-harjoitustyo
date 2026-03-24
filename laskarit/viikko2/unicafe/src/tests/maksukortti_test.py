import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_oikein_alussa(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahan_lataaminen_toimii(self):
        self.maksukortti.lataa_rahaa(200)
        self.assertEqual(self.maksukortti.saldo_euroina(), 12.0)

    def test_saldo_vahenee_oikein(self):
        self.maksukortti.ota_rahaa(200)
        self.assertEqual(self.maksukortti.saldo_euroina(), 8.0)
        
    def test_saldo_ei_muutu_jos_puuttuu(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_ota_rahaa_palauttaa_true(self):
        self.assertTrue(self.maksukortti.ota_rahaa(200))

    def test_ota_rahaa_palauttaa_false(self):
        self.assertFalse(self.maksukortti.ota_rahaa(1100))

    def test_saldo_euroissa_teksti(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")