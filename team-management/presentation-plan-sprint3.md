# Plan Présentation Orale — The Library Sprint 3

## Durée Estimée
- **Total** : 20-25 minutes (15 min présentation + 10 min questions/démo)
- **Par slide** : 2-3 minutes

---

## Slide 1 : Introduction & Contexte (2 min)

### Titre
**The Library — Sécurisation d'une application web Flask**

### Contenu
- **Équipe** : Ares (CSRF+Logging), Mohamed (Rapport/Présentation), PO (Coordination)
- **Librairie ABC** : Application gestion catalogue livres + réservations
- **Défi** : Transformer prototype non-sécurisé en app prête pour production
- **Timeframe** : 3 sprints (13 jours de dev)

### Visuels
- Logo/screenshot app
- Rôles équipe en tableau
- Dates sprints

### Speaker**
**Mohamed** (1:30 min) + transition

---

## Slide 2 : Organisation Agile (2 min)

### Titre
**Méthodologie Agile — Rôles & Workflow Git**

### Contenu
- **Rôles**
  - Product Owner : Backlog + priorités
  - Scrum Master : Planification + standups
  - Développeurs : Implementation
  - QA : Tests + sécurité
  
- **Sprints**
  - Sprint 1 (12/05) : Tests + fondations
  - Sprint 2 (19/05) : Sécurité complète
  - Sprint 3 (26/05) : UI + CSRF + Logging

- **Git Workflow**
  ```
  main (production)
    ├── feature/securite-sprint2 → PR #21-25
    ├── feature/authentification-sprint3 → PR #30
    ├── feature/interface-html-sprint3 → PR #31
    ├── feature/securite-csrf-sprint3 → PR #32
    └── docs/rapport-sprint3 → PR #33 (en cours)
  ```

### Visuels
- Tableau rôles
- Timeline sprints
- Diagramme branches git

### Speaker
**Mohamed** (2 min)

---

## Slide 3 : Analyse Initiale — Vulnérabilités (2 min)

### Titre
**Scan Bandit : 13 vulnérabilités → 0**

### Contenu
- **Sprint 1 : Diagnostic**
  - Bandit scan automatisé = 13 issues
  - HIGH : Debug mode ON, CSRF disabled, Weak crypto
  - MEDIUM : Missing headers, logging absent
  - Action items = Sprint 1-2 roadmap

- **Vulnérabilités Clés**
  | Risque | Avant | Après | Sprint |
  |--------|-------|-------|--------|
  | Debug mode | ON | OFF | Sprint 2 |
  | CSRF | Disabled | Flask-WTF | Sprint 3 |
  | Headers | Missing | CSP+X-Frame-Options | Sprint 2 |
  | Auth | Aucune | Flask-Login+bcrypt | Sprint 3 |
  | Logging | Aucune | Critique logged | Sprint 3 |

- **Outils**
  - Bandit : Security scanning
  - pytest + pytest-cov : Coverage analysis
  - SQLAlchemy ORM : SQL injection prevention

### Visuels
- Graphique 13→0 vulnérabilités
- Tableau avant/après fixes
- Bandit report snippet

### Speaker
**Mohamed** (1:30 min) + transition

---

## Slide 4 : Tests Automatiques & Couverture (2 min)

### Titre
**Progression Tests — 0 → 59 tests (85% couverture)**

### Contenu
- **Sprint 1** : 0 → 18 tests (65%)
  - test_librairie.py : 8 tests CRUD
  - test_auth.py : Inscriptions/connexions
  
- **Sprint 2** : 18 → 51 tests (82%)
  - test_securite.py : Bandit, headers, limits
  - test_reservations.py : Réservation logic
  
- **Sprint 3** : 51 → 59 tests (85%)
  - test_csrf_logging.py : 8 tests (rejet CSRF, logs)
  - Total : **59/59 passing** ✅

- **Framework**
  - pytest : Test runner + fixtures
  - pytest-cov : Coverage reporting
  - WTF_CSRF_ENABLED flag : Test config toggle

### Visuels
- Graphique progression tests (18→51→59)
- Coverage bar chart (65%→82%→85%)
- Test breakdown pie chart (auth vs livres vs securite)

### Speaker
**Ares** (2 min) - démontre test suite

```bash
$ venv\Scripts\pytest tests/ -q
========== 59 passed in 6.76s ==========
```

---

## Slide 5 : Corrections Apportées (2 min)

### Titre
**Implémentations Sécurité — de Sprint 2 à Sprint 3**

### Contenu
- **Sprint 2 : Security Hardening**
  ```python
  @app.after_request
  def set_security_headers(response):
      response.headers["X-Content-Type-Options"] = "nosniff"
      response.headers["X-Frame-Options"] = "DENY"
      response.headers["CSP"] = "default-src 'self'"
      return response
  ```
  - Debug mode disabled
  - CORS configured
  - Rate limiting (x messages/5min)

- **Sprint 3 : Auth + CSRF + Logging**
  ```python
  # Auth + bcrypt
  password_hash = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
  if bcrypt.checkpw(pwd.encode(), user.password_hash.encode()):
      login_user(user)
  
  # CSRF tokens
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
  
  # Logging
  logger.info("Connexion reussie : %s (IP: %s)", email, ip)
  logger.warning("Suppression livre : '%s' par %s", titre, user)
  ```

- **Stack Final**
  - Flask 3.0 + SQLAlchemy 3.0
  - Flask-Login + bcrypt (auth)
  - Flask-WTF (CSRF)
  - Python logging (critique actions)

### Visuels
- Code snippets sécurité
- Before/after comparison
- Dependency tree

### Speaker
**Ares** (2 min) - démontre sécurité en action

---

## Slide 6 : Architecture Finale (2 min)

### Titre
**Modèles, Routes & Blueprints**

### Contenu
- **Modèles SQLAlchemy**
  ```
  Livre : id, titre (unique), auteur, annee, disponible, reserve_par
  User  : id, email (unique), password_hash, role
  ```

- **Routes & Blueprints**
  ```
  pages_bp/
    GET    /                  → Index
    GET/POST /login           → HTML Login
    GET/POST /register        → HTML Register
    POST   /logout            → Logout
    GET    /catalogue          → Liste livres
    POST   /catalogue/*/reserver → Réservation
  
  livres_bp/ (JSON API)
    GET/POST /livres/         → CRUD
    (Exemptée CSRF)
  
  auth_bp/ (JSON API)
    POST   /auth/register     → JSON Register
    POST   /auth/login        → JSON Login
    (Exemptée CSRF)
  ```

- **Frontend**
  - Jinja2 templates
  - Tailwind CSS (responsive)
  - CSRF meta tag + hidden inputs
  - Flash messages (feedback user)

### Visuels
- Schéma ER (Livre, User)
- Diagramme routes/blueprints
- Screenshot interface HTML

### Speaker
**Mohamed** (2 min)

---

## Slide 7 : Démo Live (3-4 min)

### Titre
**Application en Action — Démo Navigateur**

### Contenu (en direct sur laptop)
1. **Démarrage app**
   ```bash
   $ flask run
   Running on http://127.0.0.1:5000
   ```

2. **Homepage** (~20 sec)
   - Page index avec CTA "Consulter Catalogue"
   - Navigation responsive (mobile/desktop)
   - Affiche "Non authentifié" dans navbar

3. **Authentification** (~1 min)
   - **Register** : Créer compte `demo@test.com` / `password123`
   - Voir logs console : `[INFO] Inscription : demo@test.com`
   - Page redirect login automatique
   - **Login** : Se connecter avec credentials
   - Voir logs : `[INFO] Connexion reussie : demo@test.com (IP: 127.0.0.1)`

4. **Catalogue & Réservation** (~1:30 min)
   - Lister livres disponibles
   - Cliquer sur livre → page détail
   - Formulaire "Réserver" avec hidden CSRF token (F12 inspect)
   - Cliquer Réserver
   - Voir logs : `[INFO] Reservation : 'Titre' par demo@test.com`
   - Livre passe en "Réservé par vous"

5. **Sécurité CSRF Test** (~30 sec)
   - Ouvrir DevTools Console
   - Faire POST sans token (curl/Postman)
   - Obtenir **400 Bad Request**
   - Montrer l'importance du token

6. **Logout** (~20 sec)
   - Cliquer Logout
   - Voir logs : `[WARNING] Deconnexion : demo@test.com`
   - Redirect index
   - Navbar affiche "Connexion"

### Checklist Avant Démo
- [ ] App running (`flask run`)
- [ ] Browser developer tools ouverts (logs visibles)
- [ ] DB seeded avec quelques livres
- [ ] Internet stable (Tailwind CDN)
- [ ] Backup plan : screenshots + vidéo enregistrée

### Visuels
- Screencast en direct
- Logs console (terminal)
- Browser inspector (CSRF token)

### Speaker
**Ares** (3-4 min) - démontre en live

---

## Slide 8 : Conclusion & Perspectives (2 min)

### Titre
**Transformation Réussie — Leçons & Avenir**

### Contenu
- **Réalisations Sprint 3**
  - ✅ Auth complète (Flask-Login + bcrypt)
  - ✅ Interface responsive (Tailwind CSS)
  - ✅ CSRF protection (Flask-WTF)
  - ✅ Logging actions critiques
  - ✅ 59 tests (85% couverture)
  - ✅ 0 vulnérabilités Bandit HIGH/MEDIUM

- **Leçons Apprises**
  1. Sécurité = itération (pasunitaire)
  2. Tests + Bandit = confiance en release
  3. Git workflow clair = collaboration efficient
  4. Documentation = onboarding rapide

- **Axes Futurs (Sprint 4+)**
  - Pagination/recherche avancée
  - CI/CD GitHub Actions
  - Docker + deployment prod
  - OAuth2 + analytics

- **Call to Action**
  - **Production ready** : Monitorer + backups
  - **Scalabilité** : Microservices si trafic ↑
  - **Maintainabilité** : Keep testing 85%+

### Visuels
- Timeline sprints (graphique)
- Achievements check-list
- Roadmap future

### Speaker
**Mohamed** (2 min) - fermeture + questions

---

## Script Présentateur (Total ~25 min)

### Timing
| Slide | Speaker | Durée | Cumulé |
|-------|---------|-------|--------|
| 1 | Mohamed | 1:30 | 1:30 |
| 2 | Mohamed | 2:00 | 3:30 |
| 3 | Mohamed | 2:00 | 5:30 |
| 4 | Ares | 2:00 | 7:30 |
| 5 | Ares | 2:00 | 9:30 |
| 6 | Mohamed | 2:00 | 11:30 |
| 7 | Ares | 3:30 | 15:00 |
| 8 | Mohamed | 2:00 | 17:00 |
| Q&A | Both | 5-10 | 22-27 |

---

## Matériel Requis
- ✅ Ordinateur (laptop présentation)
- ✅ Projecteur/écran
- ✅ Terminal avec app running
- ✅ Browser (Chrome/Firefox dev tools)
- ✅ Diaporama (PowerPoint/PDF)
- ✅ Backup : screenshots + vidéo

## Pièges à Éviter
- ❌ Démo en direct bugguée → backup screenshot
- ❌ Oublier tokens CSRF → avoir slides de code
- ❌ Parler trop vite → lire en direct du slides
- ❌ Font rendering issue → exporter en PDF

---

**Présentation Final — 26 mai 2026**  
**The Library — Sprint 3 Final Delivery**  
*Ready for jury evaluation!* 🎉
