# Spécifications fonctionnelles et techniques — The Library

> Sprint 1 | Rédigé par : Mohamed (assisté par Rudy)  
> Basé sur : [`analyse-code.md`](analyse-code.md) + sujet du prof [`variante-d.md`](variante-d.md)

---

## 1. Présentation du projet

**The Library** est une application web de gestion de bibliothèque permettant aux utilisateurs de consulter, rechercher et réserver des livres en ligne.

| Champ | Valeur |
|-------|--------|
| Nom du projet | The Library |
| Type | Application web (Python / Flask) |
| Équipe | Rudy, Diego, Ares, Mohamed |
| Méthode | Agile (sprints d'1 semaine) |

---

## 2. Fonctionnalités attendues

### 2.1 Gestion des livres (CRUD)

| ID | Fonctionnalité | Priorité |
|----|----------------|----------|
| F01 | Ajouter un livre (titre, auteur, année) | 🔴 Haute |
| F02 | Lister tous les livres | 🔴 Haute |
| F03 | Rechercher un livre par titre ou auteur | 🔴 Haute |
| F04 | Supprimer un livre | 🟠 Moyenne |
| F05 | Modifier les informations d'un livre | 🟠 Moyenne |

### 2.2 Réservations

| ID | Fonctionnalité | Priorité |
|----|----------------|----------|
| F06 | Réserver un livre (si disponible) | 🔴 Haute |
| F07 | Annuler une réservation | 🔴 Haute |
| F08 | Consulter l'historique de ses réservations | 🟠 Moyenne |
| F09 | Voir qui a réservé un livre (admin) | 🟡 Basse |

### 2.3 Gestion des utilisateurs

| ID | Fonctionnalité | Priorité |
|----|----------------|----------|
| F10 | Inscription (email, mot de passe) | 🔴 Haute |
| F11 | Connexion / Déconnexion | 🔴 Haute |
| F12 | Rôles : utilisateur standard / administrateur | 🟠 Moyenne |
| F13 | Modification du profil | 🟡 Basse |

---

## 3. Contraintes techniques

### 3.1 Stack technique

| Composant | Technologie choisie |
|-----------|---------------------|
| Backend | Python 3.14 + Flask |
| Base de données | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy |
| Authentification | Flask-Login + hash bcrypt |
| Tests | pytest |
| Analyse de code | SonarQube ou Bandit |

### 3.2 Contraintes de sécurité (issues de l'analyse)

En réponse aux vulnérabilités identifiées dans `analyse-code.md` :

| Contrainte | Description |
|------------|-------------|
| CS01 | Toutes les entrées utilisateur doivent être validées (type, longueur, format) |
| CS02 | Les mots de passe doivent être hashés (bcrypt, jamais en clair) |
| CS03 | Les routes sensibles doivent exiger une authentification |
| CS04 | Protection contre les injections XSS (échappement des sorties HTML) |
| CS05 | Protection CSRF sur tous les formulaires (Flask-WTF) |
| CS06 | Logging des actions sensibles (connexion, réservation, suppression) |
| CS07 | Pas de fonctions dangereuses (`eval`, `exec`) dans le code |

---

## 4. Architecture cible

```
The Library/
├── app.py                  ← Point d'entrée Flask
├── librairie.py            ← Logique métier (Livre, Bibliotheque)
├── models/
│   ├── livre.py            ← Modèle SQLAlchemy
│   └── utilisateur.py      ← Modèle utilisateur
├── routes/
│   ├── livres.py           ← Routes CRUD livres
│   ├── reservations.py     ← Routes réservations
│   └── auth.py             ← Routes authentification
├── templates/              ← Pages HTML (Jinja2)
├── static/                 ← CSS, JS, images
├── test_librairie.py       ← Tests unitaires
└── requirements.txt
```

---

## 5. Planning des corrections par sprint

| Sprint | Objectif | Issues concernées |
|--------|----------|-------------------|
| **Sprint 1** | Analyse, tests de sécurité, spécifications | #1, #2, #3, #4 |
| **Sprint 2** | Validation des entrées + app Flask + BDD | F01→F07, CS01→CS04 |
| **Sprint 3** | Authentification + rôles + refactoring | F10→F13, CS02, CS05 |
| **Sprint 4** | Logging + déploiement + présentation | CS06, CS07 |

---

## 6. Critères d'acceptation

Une fonctionnalité est considérée **terminée** si :
- Le code est sur une branche dédiée avec une PR
- Les tests unitaires passent (`pytest`)
- La PR a été relue et approuvée par au moins 1 membre
- Aucune vulnérabilité critique détectée par l'outil d'analyse
