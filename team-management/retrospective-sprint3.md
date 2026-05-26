# Rétrospective Sprint 3 (26 mai 2026)

## Durée Sprint
**Dates** : 22 mai — 26 mai (5 jours)  
**Objectif** : Interface HTML + CSRF + Logging  
**Statut** : ✅ 100% COMPLÉTÉ

---

## 1. Résumé Réalisations

### Issues Complétées
| # | Titre | Ares | Mohamed | Statut |
|---|-------|------|---------|--------|
| #26 | Auth Flask-Login | ✅ | - | Merged PR #30 |
| #27 | Interface HTML | - | ✅ | Merged PR #31 |
| #28 | CSRF + Logging | ✅ | - | Merged PR #32 |
| #29 | Rapport Final | - | 🔄 | En cours PR #33 |

### Livrables
- ✅ Authentication complète (Flask-Login + bcrypt)
- ✅ Interface utilisateur responsive (Tailwind CSS)
- ✅ Protection CSRF avec Flask-WTF
- ✅ Logging des actions critiques
- ✅ 8 nouveaux tests (test_csrf_logging.py)
- ✅ 59/59 tests passent

### Métriques
- **Couverture** : 51 tests → 59 tests (+8)
- **Coverage** : 82% → 85% (+3%)
- **Bandit** : 0 issues HIGH/MEDIUM ✅
- **PRs mergées** : 3/4 (dernière PR #33 en validation)

---

## 2. Ce qui a Bien Marché ✅

### Points Positifs
1. **Sécurité pro-active**
   - CSRFProtect intégré correctement dès le départ
   - Tests CSRF solides (rejet sans token)
   - Logging bien pensé (IP, actions critiques)

2. **Architecture décisionnelle**
   - Exemption CSRF par objets blueprint (pas par string) → solution elegant
   - Séparation logique routes HTML / API JSON
   - Logger hiérarchique (`the_library.pages`, `the_library.auth`)

3. **Qualité tests**
   - Fixtures `app` et `app_no_csrf` réutilisables
   - Tests logging avec `caplog` - approche robuste
   - Coverage 85% - excellente couverture

4. **Collaboration équipe**
   - PRs mergées rapidement
   - Communication claire sur bloqueurs (déni du keyword `closes`)
   - Daily standups efficaces

5. **Documentation**
   - Rapport final complet + structuré
   - Code comments explicites
   - Git history lisible

---

## 3. Points d'Amélioration 🔧

### Processus Git
**Problème** : Keyword `closes #X` dans PR description ne ferme pas auto l'issue  
**Solution appliquée** : Utiliser `gh issue close` directement  
**Pour futur** : Ajouter `closes` dans commit message (plus fiable)

```bash
# MEILLEUR
git commit -m "feat: ... (closes #28)"

# Actuellement
# PR description -> gh issue close (workaround)
```

### Sécurité CSRF
**Problème** : Exemption par string (`csrf.exempt("routes.livres.livres_bp")`) ne marche pas avec Flask-WTF  
**Solution appliquée** : Passer les objets blueprint au lieu des strings  
**Leçon** : Toujours lire la doc Flask-WTF pour les detailing d'API

```python
# ❌ Ne marche pas
csrf.exempt("routes.livres.livres_bp")

# ✅ Fonctionne
from routes.livres import livres_bp
csrf.exempt(livres_bp)
```

### Tests & Fixtures
**Observation** : Configuration `WTF_CSRF_ENABLED: False` dans fixtures est crucial  
**Amélioration** : Documenter explicitement dans docstring

```python
@pytest.fixture
def app_no_csrf():
    """App sans CSRF pour préparer données (inscriptions, logins).
    
    Nécessaire car les tests enregistrant des users avant d'activer CSRF
    doivent pouvoir POSTer sans tokens.
    """
```

---

## 4. Feedback Équipe

### Ares (CSRF + Logging)
> "CSRF a été complex initialement (exemption par string vs objets), mais bien documenté après. Tests solides, logging pratique. Prêt pour prod."

**Score Satisfaction** : 8/10  
**Blockers résolus** : 1 (exemption CSRF)

### Mohamed (Rapport + Présentation)
> "Rapport complet reflète bien le travail accompli. Sprints 2-3 montrent progression claire (0→59 tests, 13→0 vulns). Prêt pour présentation."

**Score Satisfaction** : 9/10  
**Blockers** : 0

---

## 5. Vélocité & Estimation

### Burndown Sprint 3
```
Jour 1 (22/05)  : 8 story points → 6 restant
Jour 2 (23/05)  : 6 story points → 4 restant
Jour 3 (24/05)  : 4 story points → 2 restant
Jour 4 (25/05)  : 2 story points → 1 restant (rapport)
Jour 5 (26/05)  : 1 story points → 0 (DONE) ✅
```

**Vélocité Sprint 3** : 8 points / 5 jours = **1.6 pts/jour**  
**Historique** :
- Sprint 1 : 7 pts / 3 jours = 2.3 pts/jour
- Sprint 2 : 8 pts / 4 jours = 2.0 pts/jour
- Sprint 3 : 8 pts / 5 jours = 1.6 pts/jour

**Observation** : Ralentissement Sprint 3 dû à rapport + présentation (non-tech). Vélocité dev reste stable.

---

## 6. Risques & Mitigation

| Risque | Probabilité | Impact | Mitigation | Statut |
|--------|-------------|--------|-----------|--------|
| Démo live buggée | Basse | Moyenne | Tests automatisés + manual testing | ✅ Mitigé |
| Présentation oubli slides | Très basse | Haute | Checklist 8 slides + backup PDF | ✅ Couvert |
| Regression tests | Très basse | Haute | 59 tests passent en CI | ✅ Zéro risque |
| Token CSRF expiré en démo | Basse | Basse | Refresh page = new token | ✅ OK |

---

## 7. Leçons Apprises

### Techniques
1. **Flask-WTF CSRF** : Toujours passer objets blueprint, pas strings
2. **Git keywords** : `closes` dans commit message > PR description
3. **Test fixtures** : Avoir app avec/sans CSRF pour tester inscription + POST
4. **Logging** : Inclure context (IP, utilisateur) pour debug en prod

### Processus
1. **Definition of Done** : Tests + Bandit + Logs + Documentation
2. **PR reviews** : Vérifier keywords avant merge
3. **Daily standups** : Identifie bloqueurs rapidement (exemption CSRF)

### Soft Skills
1. **Communication équipe** : Transparence sur problèmes
2. **Autonomie** : Chacun résout son issue sans attendre
3. **Qualité** : Refuser de merger sans tests/docs

---

## 8. Actions pour Sprint 4 (si applicable)

### High Priority
- [ ] Ajouter pagination catalogue (50+ livres)
- [ ] Implémentation recherche/filtrage
- [ ] CI/CD GitHub Actions (auto-test + Bandit)

### Medium Priority
- [ ] Alembic database migrations
- [ ] OpenAPI documentation
- [ ] Docker image production

### Low Priority
- [ ] OAuth2 intégration
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard

---

## 9. Célébration 🎉

### Réalisations Majeures
- ✅ **13 vulnérabilités → 0** (Bandit clean)
- ✅ **0 tests → 59 tests** (85% couverture)
- ✅ **Monolith → Architected** (blueprints, models)
- ✅ **No UI → Responsive design** (Tailwind CSS)
- ✅ **No security → Production-ready** (Auth + CSRF + Logging)

### Mention Spéciale
- **Ares** : Implementation CSRF/Logging fluide + tests complets
- **Mohamed** : Rapport structuré + organisation Agile clear

---

## 10. Recommandations Finales

### Pour la Présentation
1. **Démo live** : Tester avant (app running, DB seeded, forms POST)
2. **Backup plan** : Screenshots + vidéo enregistrée si démo crash
3. **Slides PDF** : Exporter en PDF (font rendering issues évités)
4. **Timing** : ~15 min présentation + 5 min questions

### Pour Production
1. Deployer sur Heroku/AWS avec secrets management
2. Ajouter monitoring (Sentry, DataDog)
3. Setup backups DB automatisés
4. Documentation API complète (OpenAPI)

---

**Sprint 3 terminé avec succès** ✅  
**Team morale** : Très bonne  
**Ready for presentation** : YES  
**Ready for prod** : 95% (monitoring + backups manquent)

---

*Rétrospective Sprint 3 — 26 mai 2026*  
*Équipe The Library (Ares, Mohamed, Product Owner)*
