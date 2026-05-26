"""
Tests CSRF + Logging Sprint 3 — issue #28 (Ares)
Couvre : rejet sans token CSRF, présence des logs sur actions sensibles.
"""
import logging
import pytest
from app import create_app
from models.livre import db as _db


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": True,
        "WTF_CSRF_CHECK_DEFAULT": True,
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def app_no_csrf():
    """App sans CSRF pour préparer les données (inscription, etc.)."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client_no_csrf(app_no_csrf):
    return app_no_csrf.test_client()


# --- CSRF : rejet sans token ---

def test_login_sans_csrf_rejete(client):
    """POST /login sans token CSRF → 400."""
    r = client.post("/login", data={"email": "x@x.com", "password": "mdp12345"})
    assert r.status_code == 400


def test_register_sans_csrf_rejete(client):
    """POST /register sans token CSRF → 400."""
    r = client.post("/register", data={"email": "x@x.com", "password": "mdp12345"})
    assert r.status_code == 400


def test_ajouter_livre_sans_csrf_rejete(client):
    """POST /catalogue/ajouter sans token CSRF → 400."""
    r = client.post("/catalogue/ajouter", data={
        "titre": "Test", "auteur": "Auteur", "annee_publication": "2000"
    })
    assert r.status_code == 400


def test_api_json_non_affectee_par_csrf(client):
    """L'API JSON /livres/ n'est pas affectée par CSRF (exemptée)."""
    r = client.post("/livres/", json={
        "titre": "API Test", "auteur": "Auteur", "annee_publication": 2000
    })
    assert r.status_code == 201


# --- Logging des actions sensibles ---

def test_log_connexion_succes(client_no_csrf, caplog):
    """Une connexion réussie génère un log INFO."""
    client_no_csrf.post("/register", data={"email": "alice@x.com", "password": "mdp12345"})
    with caplog.at_level(logging.INFO, logger="the_library.pages"):
        client_no_csrf.post("/login", data={"email": "alice@x.com", "password": "mdp12345"})
    assert any("Connexion reussie" in r.message for r in caplog.records)


def test_log_connexion_echec(client_no_csrf, caplog):
    """Une connexion échouée génère un log WARNING."""
    with caplog.at_level(logging.WARNING, logger="the_library.pages"):
        client_no_csrf.post("/login", data={"email": "inconnu@x.com", "password": "mdp12345"})
    assert any("Echec connexion" in r.message for r in caplog.records)


def test_log_inscription(client_no_csrf, caplog):
    """Une inscription génère un log INFO."""
    with caplog.at_level(logging.INFO, logger="the_library.pages"):
        client_no_csrf.post("/register", data={"email": "bob@x.com", "password": "mdp12345"})
    assert any("Inscription" in r.message for r in caplog.records)


def test_log_suppression(client_no_csrf, caplog):
    """Une suppression de livre génère un log WARNING."""
    # Créer un utilisateur et se connecter
    client_no_csrf.post("/register", data={"email": "admin@x.com", "password": "mdp12345"})
    client_no_csrf.post("/login", data={"email": "admin@x.com", "password": "mdp12345"})
    # Ajouter un livre
    client_no_csrf.post("/catalogue/ajouter", data={
        "titre": "A supprimer", "auteur": "Auteur", "annee_publication": "2000"
    })
    with caplog.at_level(logging.WARNING, logger="the_library.pages"):
        client_no_csrf.post("/catalogue/A supprimer/supprimer")
    assert any("Suppression livre" in r.message for r in caplog.records)
