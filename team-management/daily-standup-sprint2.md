# Daily Stand-up — Sprint 2

> Sprint 2 | 26 mai 2026

---

## Jour 1 : Lundi 26 mai 2026

### 🔴 Rudy (Scrum Master)
- ✅ **Fait** : Restructuration des issues Sprint 2 en tranches verticales (#16-#20), infrastructure Flask + SQLAlchemy + modèle Livre (PR #21 mergée)
- 🔄 **En cours** : Coordination, revue des PRs de l'équipe
- 🚧 **Bloqueurs** : Incompatibilité Flask 2.x / Werkzeug 3.x → résolu par upgrade Flask >= 3.0

### 🟢 Diego (CRUD Livres)
- ✅ **Fait** : CRUD complet `/livres/` avec validation (titres, auteurs, années), 13 tests unitaires (PR #22 mergée)
- 🔄 **En cours** : Revue des PRs réservations et sécurité
- 🚧 **Bloqueurs** : Aucun

### 🟡 Mohamed (Réservations)
- ✅ **Fait** : Routes `/livres/<titre>/reserver` et `/livres/<titre>/annuler`, champ `reserve_par` sur le modèle, 8 tests unitaires (PR #23 mergée)
- 🔄 **En cours** : Validation des tests en intégration
- 🚧 **Bloqueurs** : Migration SQLite — fichier `.db` existant sans colonne `reserve_par` → résolu en supprimant le fichier et recréant le schéma

### 🔵 Ares (Sécurité)
- ✅ **Fait** : Analyse Bandit 1.9.4 (0 issue HIGH/MEDIUM/LOW après corrections), 10 tests de sécurité dynamiques, rapport `rapport-bandit-sprint2.md` (PR #24 mergée)
- 🔄 **En cours** : Relecture du rapport final
- 🚧 **Bloqueurs** : Bandit 1.7.5 incompatible Python 3.14 (`ast.Num` supprimé) → résolu par upgrade bandit >= 1.8.0

---

## Résumé du Sprint 2

| Objectif | Statut |
|----------|--------|
| Infrastructure Flask + SQLAlchemy | ✅ Complété (PR #21) |
| CRUD Livres complet | ✅ Complété (PR #22) |
| Réservations | ✅ Complété (PR #23) |
| Sécurité Bandit + tests | ✅ Complété (PR #24) |
| Coordination + documentation | ✅ Complété (issue #20) |

**Verdict** : Sprint 2 réussi — 39/39 tests ✅, couverture 96% 🎉
