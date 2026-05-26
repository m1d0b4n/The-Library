"""
Tests logique d'accès — issue #34 (bugfix)
Couvre : suppression d'un livre réservé doit être bloquée.
"""
import pytest
from app import create_app
from models.livre import db as _db, Livre
from models.utilisateur import User
import bcrypt


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


def _register_login(client, email, password="password123"):
    client.post("/register", data={"email": email, "password": password})
    client.post("/login", data={"email": email, "password": password})


def _add_livre(client, titre="Test Livre", auteur="Auteur", annee="2000"):
    client.post("/catalogue/ajouter", data={
        "titre": titre, "auteur": auteur, "annee_publication": annee
    })


# --- Bugfix : suppression livre réservé ---

def test_suppression_livre_libre_ok(client):
    """Un livre disponible peut être supprimé."""
    _register_login(client, "alice@x.com")
    _add_livre(client, "Livre Libre")
    r = client.post("/catalogue/Livre Libre/supprimer", follow_redirects=True)
    assert b"supprim" in r.data


def test_suppression_livre_reserve_bloquee(client):
    """Un livre réservé ne peut pas être supprimé."""
    _register_login(client, "alice@x.com")
    _add_livre(client, "Livre Reserve")
    client.post("/catalogue/Livre Reserve/reserver")
    # Tenter de supprimer
    r = client.post("/catalogue/Livre Reserve/supprimer", follow_redirects=True)
    assert r.status_code == 200
    assert "Impossible de supprimer" in r.data.decode()
    # Vérifier que le livre existe toujours
    with client.application.app_context():
        assert Livre.query.filter_by(titre="Livre Reserve").first() is not None


def test_suppression_livre_reserve_par_autre_bloquee(client, app):
    """User B ne peut pas supprimer un livre réservé par User A."""
    # User A réserve le livre
    _register_login(client, "alice@x.com")
    _add_livre(client, "Livre Alice")
    client.post("/catalogue/Livre Alice/reserver")
    client.post("/logout")

    # User B tente de supprimer
    _register_login(client, "bob@x.com")
    r = client.post("/catalogue/Livre Alice/supprimer", follow_redirects=True)
    assert "Impossible de supprimer" in r.data.decode()
    with app.app_context():
        assert Livre.query.filter_by(titre="Livre Alice").first() is not None


def test_suppression_sans_auth_bloquee(client):
    """Un user non connecté ne peut pas supprimer (401)."""
    r = client.post("/catalogue/Dune/supprimer")
    assert r.status_code == 401


# --- Bugfix : modification livre réservé ---

def test_modification_livre_libre_ok(client):
    """Un livre disponible peut être modifié."""
    _register_login(client, "alice@x.com")
    _add_livre(client, "Modifiable")
    r = client.post("/catalogue/Modifiable/modifier", data={
        "auteur": "Nouvel Auteur", "annee_publication": "2010"
    }, follow_redirects=True)
    assert "Livre modifié" in r.data.decode()


def test_modification_livre_reserve_bloquee(client):
    """Un livre réservé ne peut pas être modifié."""
    _register_login(client, "alice@x.com")
    _add_livre(client, "Non Modifiable")
    client.post("/catalogue/Non Modifiable/reserver")
    r = client.post("/catalogue/Non Modifiable/modifier", data={
        "auteur": "Hacker", "annee_publication": "2010"
    }, follow_redirects=True)
    assert "Impossible de modifier" in r.data.decode()
    with client.application.app_context():
        livre = Livre.query.filter_by(titre="Non Modifiable").first()
        assert livre.auteur == "Auteur"  # inchangé
