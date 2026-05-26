# Rétrospective — Sprint 2

> Sprint 2 | 26 mai 2026

---

## Résumé du Sprint

Le Sprint 2 a consisté à implémenter l'application Flask "The Library" de A à Z, en tranches verticales indépendantes (une fonctionnalité complète par membre). Toutes les features ont été livrées avec leurs tests.

**Durée** : 1 jour intensif (26 mai 2026)  
**Objectif atteint** : ✅ Oui

---

## 📊 Métriques du Sprint

| Métrique | Valeur |
|----------|--------|
| Issues complétées | 5/5 (100%) |
| PRs créées | 4 |
| PRs mergées | 4 (100%) |
| Tests écrits | 39 |
| Tests passants | 39/39 (100%) |
| Couverture de code | 96% |
| Issues Bandit HIGH | 0 (2 corrigées) |
| Membres de l'équipe | 4 |

---

## ✅ Ce qui a bien fonctionné

1. **Tranches verticales** — Chaque membre avait une fonctionnalité complète (modèle + routes + tests), ce qui a éliminé les dépendances bloquantes entre les tâches

2. **Tests dès le départ** — Chaque PR incluait ses tests unitaires, ce qui a garanti 96% de couverture

3. **Correction proactive des vulnérabilités** — Les issues Bandit ont été corrigées dans le même PR, pas laissées en dette technique

4. **Headers de sécurité systématiques** — `X-Content-Type-Options`, `X-Frame-Options`, `CSP` ajoutés via `after_request` sur tous les blueprints

---

## 🔧 Ce qui peut être amélioré

1. **Compatibilité des dépendances vérifiée en amont** — Flask 2.x, pytest 6.x, bandit 1.7.x tous incompatibles avec Python 3.14 ; vérifier les versions avant de commencer
2. **Ne pas créer de PR avant de tester** — PR #21 créée avant de valider que l'app tournait ; toujours tester en local d'abord
3. **Migration de schéma BDD** — Prévoir un script de migration ou supprimer le `.db` explicitement lors d'ajout de colonnes
4. **`requirements.txt` maintenu à jour** — `bandit==1.7.5` était périmé ; les dépendances doivent refléter les versions réellement installées

---

## 🎯 Objectifs validés

- ✅ Application Flask fonctionnelle avec SQLAlchemy
- ✅ CRUD Livres complet avec validation métier
- ✅ Système de réservation (réserver / annuler)
- ✅ Sécurité : 0 issue Bandit HIGH, headers HTTP, tests dynamiques
- ✅ 39 tests unitaires et de sécurité, couverture 96%
- ✅ `.gitignore` propre (`.db`, `.coverage`, `venv/`)

---

## 📋 Actions pour le Sprint 3 (si applicable)

| Action | Responsable | Priorité |
|--------|-------------|----------|
| Vérifier compatibilité Python avant de choisir les versions | Rudy | 🔴 Haute |
| Ajouter `pbr` aux dépendances dans `requirements.txt` | Rudy | 🟠 Moyenne |
| Évaluer ajout d'une interface HTML ou API REST étendue | Diego | 🟡 Basse |
| Automatiser les tests en CI (GitHub Actions) | Ares | 🟡 Basse |

---

## 💬 Retours d'équipe

**Ambiance générale** : Productive et bien coordonnée — les tranches verticales ont été le bon choix 🚀
