# Rapport d'analyse de sécurité — Bandit Sprint 2

**Auteur** : Ares (issue #19)  
**Date** : Sprint 2  
**Outil** : Bandit 1.9.4  
**Python** : 3.14.0  
**Fichiers analysés** : `app.py`, `librairie.py`, `models/livre.py`, `routes/livres.py`, `routes/reservations.py`

---

## 1. Résumé exécutif

| Indicateur | Résultat |
|---|---|
| Lignes analysées | 198 |
| Issues HIGH | **0** (corrigées) |
| Issues MEDIUM | 0 |
| Issues LOW | **0** (corrigées) |
| Couverture tests | 96 % |
| Tests de sécurité | 10 / 10 ✅ |

---

## 2. Problèmes détectés et corrigés

### 2.1 B201 — Flask debug=True (HIGH — CWE-94)

**Fichier** : `app.py:35`  
**Avant** :
```python
app.run(debug=True)
```
**Après** :
```python
debug = os.environ.get("FLASK_DEBUG", "0") == "1"
app.run(debug=debug)
```
**Risque** : Le mode debug de Werkzeug expose une console Python interactive accessible depuis le navigateur, permettant l'exécution de code arbitraire sur le serveur.  
**Correction** : La valeur est désormais contrôlée par la variable d'environnement `FLASK_DEBUG`. Elle est à `0` (désactivé) par défaut.

---

### 2.2 B105 — Mot de passe codé en dur (LOW — CWE-259)

**Fichier** : `app.py:11`  
**Avant** :
```python
app.config["SECRET_KEY"] = "change-this-in-production"
```
**Après** :
```python
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(32))
```
**Risque** : Un `SECRET_KEY` fixe et connu permet la falsification des cookies de session Flask.  
**Correction** : La clé est lue depuis la variable d'environnement `SECRET_KEY`. Si elle n'est pas définie, `os.urandom(32)` génère une clé cryptographiquement aléatoire à chaque démarrage (acceptable en développement).

---

## 3. Résultat après corrections

```
Run metrics:
    Total issues (by severity):
        High:   0
        Medium: 0
        Low:    0
```

---

## 4. Tests de sécurité (`tests/test_securite.py`)

| # | Test | Critère | Statut |
|---|------|---------|--------|
| 1 | `test_pas_de_eval_dans_le_code` | Aucun `eval()`/`exec()` dans les sources (CS07) | ✅ |
| 2 | `test_xss_balise_script_titre` | Balise `<script>` retournée en JSON, non interprétée | ✅ |
| 3 | `test_xss_balise_img_auteur` | Balise `<img onerror>` stockée sans exécution | ✅ |
| 4 | `test_headers_xss_presents` | Headers `X-Content-Type-Options`, `X-Frame-Options`, `CSP` présents | ✅ |
| 5 | `test_titre_vide_rejete` | Titre vide → 422 (CS01) | ✅ |
| 6 | `test_titre_trop_long_rejete` | Titre > 200 chars → 422 (CS01) | ✅ |
| 7 | `test_annee_chaine_rejetee` | Année non entière → 422 (CS01) | ✅ |
| 8 | `test_annee_hors_limites` | Année < 1000 → 422 (CS01) | ✅ |
| 9 | `test_body_json_manquant` | Corps non-JSON → 400 | ✅ |
| 10 | `test_bandit_zero_high_severity` | Bandit automatisé — 0 issue HIGH | ✅ |

---

## 5. Protections en place (CS04)

Les headers de sécurité suivants sont ajoutés via `@livres_bp.after_request` :

- `X-Content-Type-Options: nosniff` — empêche le MIME-sniffing
- `X-Frame-Options: DENY` — protection contre le clickjacking
- `Content-Security-Policy: default-src 'self'` — restriction des sources

---

## 6. Recommandations pour la production

1. Définir `SECRET_KEY` comme variable d'environnement secrète (jamais dans le code)
2. Maintenir `FLASK_DEBUG=0` dans tous les environnements de production
3. Utiliser HTTPS (TLS) pour chiffrer les échanges
4. Relancer Bandit à chaque sprint : `bandit -r . -x venv,tests -f txt`
5. Ajouter `pbr` aux dépendances dans `requirements.txt` (dépendance de bandit)
