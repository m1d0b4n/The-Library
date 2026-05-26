# Analyse critique du code — `librairie.py`

> Sprint 1 | Réalisée par : Rudy & Diego  
> Code analysé : [`librairie.py`](../librairie.py)

---

## Résumé

Le code actuel constitue une **base fonctionnelle minimale** mais est loin d'être prêt pour une application web en production. Il manque de validation, de sécurité, de persistance et de toute logique utilisateur.

---

## Tableau des problèmes identifiés

| # | Problème | Catégorie | Sévérité |
|---|----------|-----------|----------|
| 1 | Aucune validation des entrées | Sécurité | 🔴 Critique |
| 2 | Pas d'authentification ni d'utilisateurs | Sécurité | 🔴 Critique |
| 3 | Pas de persistance des données | Architecture | 🔴 Critique |
| 4 | Pas d'application Flask (routes, API) | Architecture | 🔴 Critique |
| 5 | Pas de vérification des doublons | Logique | 🟠 Majeur |
| 6 | Réservation non liée à un utilisateur | Logique | 🟠 Majeur |
| 7 | Pas de gestion des erreurs | Qualité | 🟠 Majeur |
| 8 | Impossible de supprimer un livre | Logique | 🟡 Mineur |
| 9 | `lister_livres` retourne uniquement les titres | Qualité | 🟡 Mineur |
| 10 | `annee_publication` non validée | Qualité | 🟡 Mineur |
| 11 | Aucun logging des actions | Sécurité | 🟡 Mineur |
| 12 | `rechercher_livre` ne gère pas les homonymes | Logique | 🟡 Mineur |

---

## Détail des problèmes

### 🔴 1. Aucune validation des entrées

```python
# Actuellement — aucune vérification
def __init__(self, titre, auteur, annee_publication):
    self.titre = titre          # Peut être None, "", 999, ...
    self.auteur = auteur        # Idem
    self.annee_publication = annee_publication  # Peut être -500 ou "abc"
```

**Risque** : injections, plantages, données corrompues.  
**Correction** :
```python
def __init__(self, titre, auteur, annee_publication):
    if not isinstance(titre, str) or not titre.strip():
        raise ValueError("Le titre doit être une chaîne non vide.")
    if not isinstance(auteur, str) or not auteur.strip():
        raise ValueError("L'auteur doit être une chaîne non vide.")
    if not isinstance(annee_publication, int) or not (1000 <= annee_publication <= 2100):
        raise ValueError("L'année de publication est invalide.")
    self.titre = titre.strip()
    self.auteur = auteur.strip()
    self.annee_publication = annee_publication
    self.reserve = False
```

---

### 🔴 2. Pas d'authentification ni d'utilisateurs

Il n'existe aucun concept d'utilisateur. N'importe qui peut réserver ou annuler n'importe quel livre sans s'identifier.

**Correction à prévoir** : créer une classe `Utilisateur`, un système de sessions (Flask-Login ou JWT), et lier chaque réservation à un utilisateur.

---

### 🔴 3. Pas de persistance des données

Toutes les données sont en mémoire (`self.livres = []`). À chaque redémarrage, tout est perdu.

**Correction à prévoir** : intégrer une base de données (SQLite + SQLAlchemy ou Flask-SQLAlchemy).

---

### 🔴 4. Pas d'application Flask

Le fichier `requirements.txt` inclut Flask, mais aucune route n'existe. Il n'y a pas d'API ni d'interface web.

**Correction à prévoir** : créer un fichier `app.py` avec les routes CRUD pour les livres et les réservations.

---

### 🟠 5. Pas de vérification des doublons

```python
def ajouter_livre(self, livre):
    self.livres.append(livre)  # Aucun contrôle de doublon
```

**Correction** :
```python
def ajouter_livre(self, livre):
    if self.rechercher_livre(livre.titre):
        raise ValueError(f"Le livre '{livre.titre}' existe déjà.")
    self.livres.append(livre)
```

---

### 🟠 6. Réservation non liée à un utilisateur

```python
self.reserve = False  # Booléen simple, pas de référence à un utilisateur
```

On ne sait pas **qui** a réservé le livre.  
**Correction** : remplacer `self.reserve` par `self.reserve_par = None` (stocke l'identifiant de l'utilisateur).

---

### 🟠 7. Pas de gestion des erreurs

`rechercher_livre` retourne `None` si le livre n'est pas trouvé. Aucun appelant n'est forcé à gérer ce cas.

**Correction** : lever une exception explicite ou documenter le comportement avec des type hints.

---

### 🟡 8. Impossible de supprimer un livre

Il manque une méthode `supprimer_livre`.

---

### 🟡 9. `lister_livres` retourne uniquement les titres

```python
def lister_livres(self):
    return [livre.titre for livre in self.livres]  # Perd auteur, année, statut
```

**Correction** : retourner les objets ou des dictionnaires complets.

---

### 🟡 10. `annee_publication` non validée

Une année négative ou absurde est acceptée silencieusement.

---

### 🟡 11. Aucun logging

Aucune trace des actions effectuées (qui a réservé quoi, quand). Indispensable pour la sécurité et l'audit.

---

### 🟡 12. `rechercher_livre` ne gère pas les homonymes

Si deux livres ont le même titre, seul le premier est retourné.

---

## Priorités de correction

```
Phase 1 (Sprint 2) — Critique
  → Validation des entrées
  → Création de l'app Flask + routes de base
  → Intégration d'une base de données

Phase 2 (Sprint 3) — Majeur
  → Système d'authentification utilisateurs
  → Réservation liée à un utilisateur
  → Gestion des erreurs

Phase 3 (Sprint 3/4) — Mineur
  → Suppression de livres
  → Logging
  → Amélioration de lister_livres
```
