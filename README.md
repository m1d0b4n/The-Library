
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=F5CC27)
![Flask](https://img.shields.io/badge/Flask-3.0-F4320B?style=flat&logo=flask&logoColor=red)
![SQLite](https://img.shields.io/badge/SQLite-2780F5?style=flat&logo=sqlite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0-C809B1?style=flat&logo=tailwindcss&logoColor=purple)
![Tests](https://img.shields.io/badge/Tests-84%20passed-22C55E?style=flat&logo=pytest&logoColor=white)

```txt
         ______ ______              
       _/      Y      \_            
      // ~~ ~~ | ~~ ~  \\           The
     // ~ ~ ~~ | ~~~ ~~ \\          Library.
    //________.|.________\\         
   `----------`-'----------'        

```

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
