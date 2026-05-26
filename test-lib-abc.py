import unittest from librairie_abc import Livre, Bibliotheque

class TestBibliotheque(unittest.TestCase): def setUp(self): self.bibliotheque = Bibliotheque() self.livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943) self.bibliotheque.ajouter_livre(self.livre1)

def test_ajout_et_liste_de_livres(self):
    self.assertIn("Le Petit Prince", self.bibliotheque.lister_livres())

def test_reservation_livre(self):
    self.assertEqual(self.livre1.reserver(), "Le Petit Prince a été réservé.")
    self.assertEqual(self.livre1.reserver(), "Le Petit Prince est déjà réservé.")

def test_annulation_reservation(self):
    self.livre1.reserver()
    self.assertEqual(self.livre1.annuler_reservation(), "La réservation de Le Petit Prince a été annulée.")
    self.assertEqual(self.livre1.annuler_reservation(), "Le Petit Prince n'est pas réservé.")
if name == 'main': unittest.main()

python