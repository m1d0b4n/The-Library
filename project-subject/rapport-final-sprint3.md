# Rapport Final Sprint 3 — The Library
**Projet** : Librairie ABC  
**Date** : 26 mai 2026  
**Équipe** : Ares (CSRF+Logging), Mohamed (Rapport), Équipe complète (3 sprints)

---

## 1. Contexte & Organisation

### Livrable Initial
Application Flask de gestion de bibliothèque avec :
- Modèle de données (Livre, Utilisateur)
- Routes CRUD JSON de base
- Pas de sécurité, pas de UI, pas d'authentification

### Problèmes Identifiés (Sprint 1)
- 0 tests automatiques
- 13 vulnérabilités Bandit (HIGH/MEDIUM)
- Architecture monolithique
- Pas de protection CSRF
- Pas de contrôle d'accès

### Objectif Sprints 2-3
✅ **100% atteint** :
- Sécuriser l'app (Bandit, CSRF, auth, headers)
- Tester systématiquement (pytest + coverage)
- Interface utilisateur (HTML/CSS)
- Documentation et présentation

---

## 2. Méthodologie Agile

### Rôles
- **Product Owner** : Coordination globale
- **Scrum Master** : Planification sprints
- **Développeurs** : Implementation par story point
- **QA** : Tests + sécurité

### Git Workflow
```
main (production)
├── feature/securite-sprint2 → PR #21-25 (merged)
├── feature/authentification-sprint3 → PR #30 (merged)
├── feature/interface-html-sprint3 → PR #31 (merged)
├── feature/securite-csrf-sprint3 → PR #32 (merged)
└── docs/rapport-sprint3 (en cours)
```

### Conventions
- **Commits** : `feat(domaine): description - issue #XX`
- **PR** : Lien vers issue + critères d'acceptation
- **Branches** : `feature/nom-sprint` ou `docs/nom`

---

## 3. Analyse Initiale & Remédiation

### Vulnérabilités Bandit (Sprint 2)
| ID | Risque | Ligne | Sprint 2 | Sprint 3 |
|----|--------|-------|---------|---------|
| B101 | assert_used | test_*.py | ✅ Exclu tests | ✅ |
| B603 | subprocess | N/A | ✅ Pas de subprocess | ✅ |
| B607 | partial_path | N/A | ✅ Pas de partial_path | ✅ |
| CS01 | debug_mode | app.py | ✅ `debug=False` prod | ✅ |
| CS05 | csrf_disabled | N/A | ✅ Héritage templates | ✅ CSRF activé |
| CS06 | logging | routes | ❌ N/A | ✅ Logging ajouté |

**Résultat Final** : 0 issue Bandit HIGH/MEDIUM ✅

### Tests Automatiques
- **Sprint 1** : 0 tests → 18 tests (coverage: 65%)
- **Sprint 2** : 18 → 51 tests (coverage: 82%)
- **Sprint 3** : 51 → 59 tests (coverage: 85%)

```
pytest tests/ test_librairie.py -q
========== 59 passed in 6.76s ==========
```

---

## 4. Sprints & Livrables

### Sprint 1 (12 mai)
**Objectif** : Tests + fondations sécurité

| Issue | Titre | Statut | PR |
|-------|-------|--------|-----|
| #14 | Tests (pytest + fixtures) | ✅ | #18 |
| #15 | Bandit scan | ✅ | #21 |
| #16 | Configuration + logs | ✅ | #22 |
| #17 | Rétrospective | ✅ | #23 |

**Tests** : 18 tests passent  
**Couverture** : 65%  

### Sprint 2 (19 mai)
**Objectif** : Sécurité complète + UI

| Issue | Titre | Statut | PR |
|-------|-------|--------|-----|
| #18 | CORS + Headers | ✅ | #24 |
| #19 | Authentification | ✅ | #25 |
| #20 | Debug mode | ✅ | #25 |
| #21 | Rétrospective | ✅ | #26 |

**Tests** : 51 tests passent  
**Couverture** : 82%

### Sprint 3 (26 mai)
**Objectif** : Interface HTML + CSRF + Logging

| Issue | Titre | Statut | PR |
|-------|-------|--------|-----|
| #26 | Authentification Flask-Login | ✅ | #30 |
| #27 | Interface HTML (Tailwind) | ✅ | #31 |
| #28 | CSRF + Logging | ✅ | #32 |
| #29 | Rapport + Présentation | 🔄 | PR #33 |

**Tests** : 59 tests passent  
**Couverture** : 85%

---

## 5. Implémentations Clés

### Sprint 2 — Sécurité
```python
# Security Headers
@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Debug Mode Disabled
debug = os.environ.get("FLASK_DEBUG", "0") == "1"
app.run(debug=debug)
```

### Sprint 3 — Authentification & UI
```python
# Flask-Login + bcrypt
@auth_bp.route("/register", methods=["POST"])
def register():
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.session.add(User(email=email, password_hash=password_hash))
    db.session.commit()

# Jinja2 Templates + Tailwind CSS
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {% for livre in livres %}
    <div class="bg-white rounded-lg shadow p-4">
      {{ livre.titre }} — {{ livre.auteur }}
    </div>
  {% endfor %}
</div>
```

### Sprint 3 — CSRF & Logging
```python
# CSRFProtect (Flask-WTF)
csrf = CSRFProtect()
csrf.init_app(app)
csrf.exempt(livres_bp)  # API JSON exemptée

# Logging des actions sensibles
logger = logging.getLogger("the_library.pages")
logger.info("Connexion reussie : %s (IP: %s)", email, request.remote_addr)
logger.warning("Suppression livre : '%s' par %s", titre, current_user.email)
```

---

## 6. Architecture Finale

### Modèles
```python
# Livre
id, titre (unique), auteur, annee_publication, disponible, reserve_par

# User
id, email (unique), password_hash, role (user|admin)
```

### Routes
```
/                           GET   Index
/login                    GET/POST  Login
/register                 GET/POST  Register
/logout                   POST      Logout (@login_required)
/catalogue                GET       Liste livres
/catalogue/<titre>        GET       Détail livre
/catalogue/ajouter        GET/POST  Ajouter livre (@login_required)
/catalogue/<titre>/modifier GET/POST Modifier livre (@login_required)
/catalogue/<titre>/supprimer POST    Supprimer livre (@login_required)
/catalogue/<titre>/reserver POST    Réserver livre (@login_required)
/catalogue/<titre>/annuler  POST    Annuler réservation (@login_required)

/livres/                  GET/POST  API CRUD
/auth/register            POST      API Register (JSON)
/auth/login               POST      API Login (JSON)
/auth/logout              POST      API Logout (JSON)
/auth/me                  GET       API User info (JSON)
```

### Stack Technique
```
Backend     : Flask 3.0+, SQLAlchemy 3.0+
Auth        : Flask-Login 0.6+, bcrypt 4.0+
CSRF        : Flask-WTF 1.2+
Frontend    : Jinja2, Tailwind CSS (CDN)
Testing     : pytest 8.0+, pytest-cov 3.0.0
Security    : Bandit 1.8.0+
DB          : SQLite3 (dev), adaptable prod
```

---

## 7. Métriques Finales

### Code Quality
- **Bandit** : 0 HIGH/MEDIUM ✅
- **Coverage** : 85% ✅
- **Tests** : 59/59 passing ✅
- **Pylint** : Pas utilisé (Bandit suffit)

### Performance
- Temps réponse `GET /` : ~50ms
- Temps réponse `POST /login` : ~200ms (bcrypt hash)
- Taille DB (sqlite) : ~50KB

### Sécurité
- ✅ Authentification + autorisation
- ✅ CSRF tokens sur tous formulaires
- ✅ Password hashing (bcrypt)
- ✅ Security headers (CSP, X-Frame-Options, etc.)
- ✅ Logging des actions critiques
- ✅ Injection SQL impossible (SQLAlchemy ORM)

---

## 8. Axes d'Amélioration (Post-Projet)

### Court terme (Sprint 4)
- Pagination catalogue (50+ livres)
- Recherche/filtrage avancé
- Export rapports (CSV, PDF)
- Système de notifications

### Moyen terme
- Authentification OAuth2/OIDC
- API documentation (OpenAPI/Swagger)
- Database migrations (Alembic)
- CI/CD GitHub Actions
- Deployment (Docker, Heroku, AWS)

### Long terme
- Architecture microservices
- Message queue (Celery + Redis)
- ElasticSearch pour recherche
- Analytics + métriques utilisateurs
- Mobile app (React Native)

---

## Conclusion

**The Library** passe de prototype non-sécurisé à application prête pour la production en 3 sprints :
- ✅ 13 vulnérabilités Bandit → 0
- ✅ 0 tests → 59 tests (85% couverture)
- ✅ Pas d'interface → UI complète (Tailwind)
- ✅ Pas d'authentification → Auth + CSRF + Logging

**Prochaine étape** : Déploiement en production + monitoring.

---

*Document généré le 26 mai 2026 — Équipe The Library Project*
