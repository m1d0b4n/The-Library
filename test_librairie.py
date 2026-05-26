import unittest
from librairie import Livre, Bibliotheque


class TestBibliotheque(unittest.TestCase):
    def setUp(self):
        self.bibliotheque = Bibliotheque()
        self.livre1 = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943)
        self.bibliotheque.ajouter_livre(self.livre1)

    def test_ajout_et_liste_de_livres(self):
        self.assertIn("Le Petit Prince", self.bibliotheque.lister_livres())

    def test_reservation_livre(self):
        self.assertEqual(self.livre1.reserver(), "Le Petit Prince a été réservé.")
        self.assertEqual(self.livre1.reserver(), "Le Petit Prince est déjà réservé.")

    def test_annulation_reservation(self):
        self.livre1.reserver()
        self.assertEqual(self.livre1.annuler_reservation(), "La réservation de Le Petit Prince a été annulée.")
        self.assertEqual(self.livre1.annuler_reservation(), "Le Petit Prince n'est pas réservé.")

    def test_limite_titre_vide(self):
        livre_vide = Livre("", "", None)
        self.bibliotheque.ajouter_livre(livre_vide)
        self.assertIn("", self.bibliotheque.lister_livres())

    def test_injection_xss(self):
        livre_xss = Livre("<script>alert('XSS')</script>", "Attaquant", 2023)
        self.bibliotheque.ajouter_livre(livre_xss)
        self.assertIn("<script>alert('XSS')</script>", self.bibliotheque.lister_livres())

    def test_recherche_inexistante(self):
        resultat = self.bibliotheque.rechercher_livre("Livre Inconnu")
        self.assertIsNone(resultat)

    def test_type_invalide(self):
        livre_int = Livre(12345, "Auteur", 2021)
        self.bibliotheque.ajouter_livre(livre_int)
        # Ceci causera un crash AttributeError car int n'a pas de methode .lower()
        with self.assertRaises(AttributeError):
            self.bibliotheque.rechercher_livre("12345")

    def test_analyse_statique(self):
        import ast
        with open("librairie.py", "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            # Check for dangerous functions like eval or exec
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, ['eval', 'exec'], "Fonction dangereuse trouvée !")

if __name__ == '__main__':
    unittest.main()
