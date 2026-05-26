import pytest
import bcrypt
from app import create_app
from models.livre import db
from models.utilisateur import User
from models.livre import Livre


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def _make_user(app, email, password="password123", role="user"):
    with app.app_context():
        pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(email=email, password_hash=pw, role=role)
        db.session.add(user)
        db.session.commit()
        return user.id


def _login(client, email, password="password123"):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


# --- Setup first-run ---

def test_setup_cree_admin_si_aucun_user(app, client):
    resp = client.post("/setup", data={"email": "admin@test.com", "password": "adminpass"}, follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email="admin@test.com").first()
        assert user is not None
        assert user.role == "admin"


def test_setup_bloque_si_user_existe(app, client):
    _make_user(app, "existant@test.com", role="user")
    resp = client.post("/setup", data={"email": "admin2@test.com", "password": "adminpass"})
    assert resp.status_code == 403


def test_setup_email_invalide(app, client):
    resp = client.post("/setup", data={"email": "", "password": "adminpass"}, follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert User.query.count() == 0


def test_setup_password_trop_court(app, client):
    resp = client.post("/setup", data={"email": "admin@test.com", "password": "court"}, follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert User.query.count() == 0


# --- Admin : accès ---

def test_admin_dashboard_interdit_non_connecte(app, client):
    resp = client.get("/admin/", follow_redirects=False)
    assert resp.status_code == 302


def test_admin_dashboard_interdit_user_normal(app, client):
    _make_user(app, "user@test.com", role="user")
    _login(client, "user@test.com")
    resp = client.get("/admin/")
    assert resp.status_code == 403


def test_admin_dashboard_accessible_admin(app, client):
    _make_user(app, "admin@test.com", role="admin")
    _login(client, "admin@test.com")
    resp = client.get("/admin/")
    assert resp.status_code == 200


# --- Admin : livres ---

def test_admin_peut_supprimer_livre_reserve(app, client):
    _make_user(app, "admin@test.com", role="admin")
    with app.app_context():
        livre = Livre(titre="Livre Réservé", auteur="X", annee_publication=2000, disponible=False, reserve_par="autre@test.com")
        db.session.add(livre)
        db.session.commit()
    _login(client, "admin@test.com")
    resp = client.post("/admin/livres/Livre Réservé/supprimer", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert Livre.query.filter_by(titre="Livre Réservé").first() is None


def test_user_normal_ne_peut_pas_supprimer_via_admin(app, client):
    _make_user(app, "user@test.com", role="user")
    with app.app_context():
        livre = Livre(titre="Livre Normal", auteur="X", annee_publication=2000)
        db.session.add(livre)
        db.session.commit()
    _login(client, "user@test.com")
    resp = client.post("/admin/livres/Livre Normal/supprimer")
    assert resp.status_code == 403


# --- Admin : users ---

def test_admin_peut_promouvoir_user(app, client):
    admin_id = _make_user(app, "admin@test.com", role="admin")
    user_id = _make_user(app, "user@test.com", role="user")
    _login(client, "admin@test.com")
    resp = client.post(f"/admin/users/{user_id}/toggle-admin", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        user = db.session.get(User, user_id)
        assert user.role == "admin"


def test_admin_peut_revoquer_admin(app, client):
    _make_user(app, "admin@test.com", role="admin")
    other_id = _make_user(app, "other@test.com", role="admin")
    _login(client, "admin@test.com")
    resp = client.post(f"/admin/users/{other_id}/toggle-admin", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        user = db.session.get(User, other_id)
        assert user.role == "user"


def test_admin_ne_peut_pas_modifier_son_propre_role(app, client):
    admin_id = _make_user(app, "admin@test.com", role="admin")
    _login(client, "admin@test.com")
    resp = client.post(f"/admin/users/{admin_id}/toggle-admin", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        user = db.session.get(User, admin_id)
        assert user.role == "admin"


def test_admin_peut_supprimer_user(app, client):
    _make_user(app, "admin@test.com", role="admin")
    user_id = _make_user(app, "victim@test.com", role="user")
    _login(client, "admin@test.com")
    resp = client.post(f"/admin/users/{user_id}/supprimer", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert db.session.get(User, user_id) is None


def test_admin_ne_peut_pas_supprimer_son_propre_compte(app, client):
    admin_id = _make_user(app, "admin@test.com", role="admin")
    _login(client, "admin@test.com")
    resp = client.post(f"/admin/users/{admin_id}/supprimer", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert db.session.get(User, admin_id) is not None


# --- is_admin property ---

def test_is_admin_property(app):
    with app.app_context():
        admin = User(email="a@a.com", password_hash="x", role="admin")
        user = User(email="b@b.com", password_hash="x", role="user")
        assert admin.is_admin is True
        assert user.is_admin is False
