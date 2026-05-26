# Daily Standup — Sprint 3 (26 mai 2026)

## Status: COMPLETED ✅

---

## Membres & Tâches

### Ares (CSRF + Logging)
**Assignée** : Issue #28  
**Branche** : `feature/securite-csrf-sprint3`  
**PR** : #32 (Merged)

#### Progression
- ✅ Flask-WTF installé + CSRFProtect intégré
- ✅ Tokens CSRF dans tous formulaires HTML (6 formulaires)
- ✅ API JSON exemptées CSRF (livres_bp, reservations_bp, auth_bp)
- ✅ Logger configuré + logs sur actions sensibles (connexion, inscription, suppression, réservation)
- ✅ 8 nouveaux tests (test_csrf_logging.py)
- ✅ requirements.txt mis à jour
- ✅ 59/59 tests passent

**Blockers** : Aucun  
**Next** : Issue #29 — Rapport final

---

### Mohamed (Rapport + Présentation)
**Assignée** : Issue #29  
**Branche** : `docs/rapport-sprint3`  
**PR** : #33 (en cours)

#### Progression
- ✅ Rapport final rédigé (rapport-final-sprint3.md)
  - Contexte & organisation Agile
  - Analyse vulnérabilités Bandit (résolu)
  - Tests & couverture (18 → 51 → 59)
  - Sprints 1-3 : livrables + PR
  - Architecture finale + stack tech
  - Métriques finales
  - Axes d'amélioration

**En cours**
- Daily standup Sprint 3 (ce document)
- Rétrospective finale
- Plan diaporama 8 slides

**Next**
- Rédiger 8 slides présentation orale
- Assembler daily standup + rétrospective
- Push PR #33

---

## État Global Sprint 3

### Issues
| # | Titre | Statut | PR | Mergé |
|---|-------|--------|----|----|
| #26 | Auth Flask-Login | ✅ | #30 | ✅ |
| #27 | Interface HTML | ✅ | #31 | ✅ |
| #28 | CSRF + Logging | ✅ | #32 | ✅ |
| #29 | Rapport + Présentation | 🔄 | #33 | ⏳ |

### Risques & Dépendances
- ✅ 0 dépendances bloquantes
- ✅ Toutes les PRs mergées sauf #33
- ✅ Présentations en préparation

### Métriques
- **Tests** : 59/59 passing
- **Couverture** : 85%
- **Bandit** : 0 HIGH/MEDIUM
- **Branches actives** : `docs/rapport-sprint3`

---

## À faire avant présentation (< 2h)
- [ ] Finaliser 8 slides diaporama
- [ ] Assembler rétrospective Sprint 3
- [ ] Merge PR #33
- [ ] Tester démo live (app flask + navigateur)
- [ ] Préparer backup présentation (PDF + pptx)

---

**Date** : 26 mai 2026, 14h00  
**Scrum Master** : Coordination  
**Prochaine standup** : Avant présentation orale
