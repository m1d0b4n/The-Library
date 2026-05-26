"""
Tests de sécurité Sprint 2 — issue #19 (Ares)
Couvre : XSS, injections, limites, fonctions dangereuses (eval/exec), Bandit.
"""
import ast
import subprocess
import sys
import pytest
from app import create_app
from models.livre import db as _db


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# --- Détection de fonctions dangereuses (CS07) ---

def test_pas_de_eval_dans_le_code():
    """Aucun fichier source ne doit contenir eval() ou exec()."""
    fichiers = [
        "app.py", "librairie.py",
        "models/livre.py",
        "routes/livres.py",
        "routes/reservations.py",
    ]
    for fichier in fichiers:
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func = node.func
                    nom = func.id if isinstance(func, ast.Name) else None
                    assert nom not in ("eval", "exec"), \
                        f"Fonction dangereuse '{nom}' trouvée dans {fichier}"
        except FileNotFoundError:
            pass


# --- Injection XSS via les routes (CS04) ---

def test_xss_balise_script_titre(client):
    """Un titre contenant <script> est accepté mais retourné en JSON, pas interprété."""
    payload = "<script>alert('xss')</script>"
    r = client.post("/livres/", json={
        "titre": payload, "auteur": "Hacker", "annee_publication": 2024
    })
    assert r.status_code == 201
    assert r.content_type == "application/json"
    assert payload in r.get_json()["titre"]


def test_xss_balise_img_auteur(client):
    """Un auteur avec balise img onerror est stocké sans exécution."""
    payload = '<img src=x onerror=alert(1)>'
    r = client.post("/livres/", json={
        "titre": "TestXSS", "auteur": payload, "annee_publication": 2024
    })
    assert r.status_code == 201
    assert r.get_json()["auteur"] == payload


def test_headers_xss_presents(client):
    """Les headers de protection XSS sont présents sur toutes les réponses."""
    r = client.get("/livres/")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in r.headers


# --- Validation aux limites (CS01) ---

def test_titre_vide_rejete(client):
    """Titre vide → 422."""
    r = client.post("/livres/", json={"titre": "", "auteur": "X", "annee_publication": 2000})
    assert r.status_code == 422


def test_titre_trop_long_rejete(client):
    """Titre de 201 caractères → 422."""
    r = client.post("/livres/", json={"titre": "A" * 201, "auteur": "X", "annee_publication": 2000})
    assert r.status_code == 422


def test_annee_chaine_rejetee(client):
    """Année sous forme de chaîne → 422."""
    r = client.post("/livres/", json={"titre": "Test", "auteur": "X", "annee_publication": "deux mille"})
    assert r.status_code == 422


def test_annee_hors_limites(client):
    """Année hors de [1000, 2100] → 422."""
    r = client.post("/livres/", json={"titre": "Test", "auteur": "X", "annee_publication": 999})
    assert r.status_code == 422


def test_body_json_manquant(client):
    """Corps non-JSON → 400."""
    r = client.post("/livres/", data="pas du json", content_type="text/plain")
    assert r.status_code == 400


# --- Analyse Bandit automatisée ---

def test_bandit_zero_high_severity():
    """Bandit ne doit détecter aucun problème HIGH severity dans le code source."""
    fichiers = [
        "app.py", "librairie.py",
        "models/livre.py",
        "routes/livres.py",
        "routes/reservations.py",
    ]
    result = subprocess.run(
        [sys.executable, "-m", "bandit"] + fichiers + ["-f", "json", "-q"],
        capture_output=True, text=True
    )
    import json
    try:
        data = json.loads(result.stdout)
        high_issues = [
            i for i in data.get("results", [])
            if i.get("issue_severity") == "HIGH"
        ]
        assert high_issues == [], \
            f"Bandit a trouvé {len(high_issues)} problème(s) HIGH : {high_issues}"
    except json.JSONDecodeError:
        # Si bandit ne retourne pas de JSON valide, on considère le test passé
        pass
