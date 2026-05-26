class Livre: def init(self, titre, auteur, annee_publication): self.titre = titre self.auteur = auteur self.annee_publication = annee_publication self.reserve = False

def reserver(self):
    if not self.reserve:
        self.reserve = True
        return f"{self.titre} a été réservé."
    else:
        return f"{self.titre} est déjà réservé."

def annuler_reservation(self):
    if self.reserve:
        self.reserve = False
        return f"La réservation de {self.titre} a été annulée."
    else:
        return f"{self.titre} n'est pas réservé."
class Bibliotheque: def init(self): self.livres = []

def ajouter_livre(self, livre):
    self.livres.append(livre)

def lister_livres(self):
    return [livre.titre for livre in self.livres]

def rechercher_livre(self, titre):
    for livre in self.livres:
        if livre.titre.lower() == titre.lower():
            return livre
    return None