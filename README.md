# The Library

Application de gestion de bibliothèque en Python.

## Structure du projet

```
The Library/
├── librairie.py        # Classes Livre et Bibliotheque
├── test_librairie.py   # Tests unitaires
└── requirements.txt    # Dépendances
```

## Installation

### 1. Créer un environnement virtuel (recommandé)

```bash
py -m venv venv
venv\Scripts\activate   # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer les tests

```bash
pytest test_librairie.py
```

Ou avec le module unittest :

```bash
py -m unittest test_librairie.py
```

## Utilisation du module

```python
from librairie import Livre, Bibliotheque

# Créer une bibliothèque
biblio = Bibliotheque()

# Ajouter des livres
livre = Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943)
biblio.ajouter_livre(livre)

# Lister les livres
print(biblio.lister_livres())

# Rechercher un livre
result = biblio.rechercher_livre("Le Petit Prince")

# Réserver / annuler une réservation
print(result.reserver())
print(result.annuler_reservation())
```
