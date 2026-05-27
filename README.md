# The Library

Application web de gestion de bibliothèque développée avec Flask.

## Fonctionnalités

- Catalogue des livres (titre, auteur, année, image de couverture)
- Réservation et annulation de réservation
- Authentification (inscription / connexion)
- Panel d'administration (gestion des utilisateurs et des livres)
- Upload et compression automatique des images de couverture
- Protection CSRF sur tous les formulaires

## Structure du projet

```
The Library/
├── app.py                  # Factory Flask (création de l'app)
├── models/
│   ├── livre.py            # Modèle Livre (SQLAlchemy)
│   └── utilisateur.py      # Modèle Utilisateur (SQLAlchemy + Flask-Login)
├── routes/
│   ├── pages.py            # Routes principales (catalogue, détail, CRUD livres)
│   ├── auth.py             # Routes authentification (inscription, connexion)
│   ├── reservations.py     # Routes réservations
│   ├── admin.py            # Routes panel admin
│   └── livres.py           # Routes API livres
├── templates/
│   ├── base.html           # Template de base
│   └── livres/             # Templates catalogue, détail, formulaire
├── static/
│   └── uploads/livres/     # Images de couverture uploadées (non versionné)
├── tests/                  # Suite de tests pytest (84 tests)
├── requirements.txt        # Dépendances Python
└── instance/               # Base de données SQLite (non versionnée)
```

## Installation

### 1. Créer un environnement virtuel

```bash
py -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux / macOS
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
pip install pillow
```

### 3. Lancer l'application

```bash
py app.py
```

L'application est accessible sur [http://localhost:5000](http://localhost:5000).

## Accès administrateur

Au premier lancement, aucun compte admin n'existe. Pour en créer un :

1. Se rendre sur [http://localhost:5000/admin/setup](http://localhost:5000/admin/setup)
2. Créer le compte administrateur
3. Cette page est désactivée dès qu'un admin existe

## Lancer les tests

```bash
pytest tests/
```

Avec le rapport de couverture :

```bash
pytest tests/ --cov=. --cov-report=term-missing
```
