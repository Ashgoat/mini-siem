import unittest

from detection import compter_tentatives, detecter_brute_force


class TestDetection(unittest.TestCase):

    # TEST 1 : compter plusieurs tentatives depuis une IP
    def test_compter_tentatives(self):

        lignes = [
            "Failed password for admin from 192.168.1.10",
            "Failed password for admin from 192.168.1.10",
            "Failed password for admin from 192.168.1.10"
        ]

        resultat = compter_tentatives(lignes)

        attendu = {
            "192.168.1.10": 3
        }

        self.assertEqual(resultat, attendu)


    # TEST 2 : ignorer les connexions réussies
    def test_connexion_reussie(self):

        lignes = [
            "Accepted password for admin from 192.168.1.10"
        ]

        resultat = compter_tentatives(lignes)

        attendu = {}

        self.assertEqual(resultat, attendu)


    # TEST 3 : compter plusieurs adresses IP
    def test_plusieurs_ip(self):

        lignes = [
            "Failed password for admin from 192.168.1.10",
            "Failed password for admin from 192.168.1.20",
            "Failed password for admin from 192.168.1.20"
        ]

        resultat = compter_tentatives(lignes)

        attendu = {
            "192.168.1.10": 1,
            "192.168.1.20": 2
        }

        self.assertEqual(resultat, attendu)


    # TEST 4 : détecter un brute force
    def test_brute_force_detecte(self):

        tentatives = {
            "192.168.1.10": 5
        }

        resultat = detecter_brute_force(tentatives)

        attendu = {
            "192.168.1.10": 5
        }

        self.assertEqual(resultat, attendu)


    # TEST 5 : ignorer une IP sous le seuil
    def test_brute_force_non_detecte(self):

        tentatives = {
            "192.168.1.10": 3
        }

        resultat = detecter_brute_force(tentatives)

        attendu = {}

        self.assertEqual(resultat, attendu)


if __name__ == "__main__":
    unittest.main()