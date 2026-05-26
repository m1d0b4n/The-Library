"""
Tests d'authentification Sprint 3 — issue #26 (Rudy)
Couvre : inscription, connexion, déconnexion, accès protégé, doublons, validation.
"""
import pytest
from app import create_app
from models.livre import db as _db


@pytest.fixture
def app():
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


# --- Inscription ---

def test_inscription_succes(client):
    r = client.post("/auth/register", json={
        "email": "alice@example.com", "password": "motdepasse123"
    })
    assert r.status_code == 201
    data = r.get_json()
    assert data["email"] == "alice@example.com"
    assert data["role"] == "user"
    assert "password_hash" not in data


def test_inscription_email_doublon(client):
    client.post("/auth/register", json={"email": "alice@example.com", "password": "motdepasse123"})
    r = client.post("/auth/register", json={"email": "alice@example.com", "password": "autremotdepasse"})
    assert r.status_code == 409


def test_inscription_email_vide(client):
    r = client.post("/auth/register", json={"email": "", "password": "motdepasse123"})
    assert r.status_code == 422


def test_inscription_mot_de_passe_trop_court(client):
    r = client.post("/auth/register", json={"email": "bob@example.com", "password": "court"})
    assert r.status_code == 422


def test_inscription_sans_json(client):
    r = client.post("/auth/register", data="pas du json", content_type="text/plain")
    assert r.status_code == 400


# --- Connexion ---

def test_connexion_succes(client):
    client.post("/auth/register", json={"email": "alice@example.com", "password": "motdepasse123"})
    r = client.post("/auth/login", json={"email": "alice@example.com", "password": "motdepasse123"})
    assert r.status_code == 200
    assert r.get_json()["email"] == "alice@example.com"


def test_connexion_mauvais_mot_de_passe(client):
    client.post("/auth/register", json={"email": "alice@example.com", "password": "motdepasse123"})
    r = client.post("/auth/login", json={"email": "alice@example.com", "password": "mauvais"})
    assert r.status_code == 401


def test_connexion_email_inexistant(client):
    r = client.post("/auth/login", json={"email": "inconnu@example.com", "password": "motdepasse123"})
    assert r.status_code == 401


# --- Routes protégées ---

def test_logout_sans_connexion(client):
    r = client.post("/auth/logout")
    assert r.status_code == 401


def test_me_sans_connexion(client):
    r = client.get("/auth/me")
    assert r.status_code == 401


def test_me_connecte(client):
    client.post("/auth/register", json={"email": "alice@example.com", "password": "motdepasse123"})
    client.post("/auth/login", json={"email": "alice@example.com", "password": "motdepasse123"})
    r = client.get("/auth/me")
    assert r.status_code == 200
    assert r.get_json()["email"] == "alice@example.com"


def test_logout_connecte(client):
    client.post("/auth/register", json={"email": "alice@example.com", "password": "motdepasse123"})
    client.post("/auth/login", json={"email": "alice@example.com", "password": "motdepasse123"})
    r = client.post("/auth/logout")
    assert r.status_code == 200
    # Après déconnexion, /auth/me doit retourner 401
    r2 = client.get("/auth/me")
    assert r2.status_code == 401
