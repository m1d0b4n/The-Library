import io
import os
import pytest
import bcrypt
from PIL import Image
from app import create_app
from models.livre import db, Livre
from models.utilisateur import User


@pytest.fixture
def app(tmp_path):
    upload_dir = tmp_path / "uploads" / "livres"
    upload_dir.mkdir(parents=True)
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret",
        "UPLOAD_FOLDER": str(upload_dir),
        "MAX_CONTENT_LENGTH": 2 * 1024 * 1024,
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


# --- Helpers pour créer des fichiers image de test ---

def _png_bytes():
    """PNG 1x1 pixel valide généré par Pillow."""
    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color=(255, 0, 0)).save(buf, format="PNG")
    return buf.getvalue()


def _fake_bytes():
    """Faux fichier déguisé en PNG mais contenu invalide."""
    return b'not an image at all'


# --- Tests upload image lors de la création ---

def test_ajouter_livre_sans_image(app, client):
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    resp = client.post("/catalogue/ajouter", data={
        "titre": "Livre Sans Image",
        "auteur": "Auteur",
        "annee_publication": "2020",
    }, follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        livre = Livre.query.filter_by(titre="Livre Sans Image").first()
        assert livre is not None
        assert livre.image_filename is None


def test_ajouter_livre_avec_image_png_valide(app, client):
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    resp = client.post("/catalogue/ajouter", data={
        "titre": "Livre Avec Image",
        "auteur": "Auteur",
        "annee_publication": "2021",
        "image": (io.BytesIO(_png_bytes()), "cover.png"),
    }, content_type="multipart/form-data", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        livre = Livre.query.filter_by(titre="Livre Avec Image").first()
        assert livre is not None
        assert livre.image_filename is not None
        assert livre.image_filename.endswith(".png")
        # Le fichier doit exister sur le disque
        chemin = os.path.join(app.config["UPLOAD_FOLDER"], livre.image_filename)
        assert os.path.isfile(chemin)


def test_ajouter_livre_image_extension_invalide(app, client):
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    resp = client.post("/catalogue/ajouter", data={
        "titre": "Livre Bad Ext",
        "auteur": "Auteur",
        "annee_publication": "2021",
        "image": (io.BytesIO(b"data"), "script.exe"),
    }, content_type="multipart/form-data", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert Livre.query.filter_by(titre="Livre Bad Ext").first() is None


def test_ajouter_livre_image_contenu_invalide(app, client):
    """Extension PNG mais contenu non-image."""
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    resp = client.post("/catalogue/ajouter", data={
        "titre": "Livre Fake PNG",
        "auteur": "Auteur",
        "annee_publication": "2021",
        "image": (io.BytesIO(_fake_bytes()), "fake.png"),
    }, content_type="multipart/form-data", follow_redirects=True)
    assert resp.status_code == 200
    with app.app_context():
        assert Livre.query.filter_by(titre="Livre Fake PNG").first() is None


# --- Tests upload image lors de la modification ---

def test_modifier_livre_remplace_image(app, client):
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    # Créer avec une image
    client.post("/catalogue/ajouter", data={
        "titre": "Livre Modif",
        "auteur": "Auteur",
        "annee_publication": "2020",
        "image": (io.BytesIO(_png_bytes()), "first.png"),
    }, content_type="multipart/form-data")

    with app.app_context():
        livre = Livre.query.filter_by(titre="Livre Modif").first()
        ancien_nom = livre.image_filename

    # Modifier avec une nouvelle image
    resp = client.post("/catalogue/Livre Modif/modifier", data={
        "titre": "Livre Modif",
        "auteur": "Nouvel Auteur",
        "annee_publication": "2021",
        "image": (io.BytesIO(_png_bytes()), "second.png"),
    }, content_type="multipart/form-data", follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        livre = Livre.query.filter_by(titre="Livre Modif").first()
        assert livre.image_filename != ancien_nom
        # L'ancienne image doit avoir été supprimée
        chemin_ancien = os.path.join(app.config["UPLOAD_FOLDER"], ancien_nom)
        assert not os.path.isfile(chemin_ancien)


def test_modifier_livre_sans_nouvelle_image_conserve_ancienne(app, client):
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    client.post("/catalogue/ajouter", data={
        "titre": "Livre Conserve",
        "auteur": "Auteur",
        "annee_publication": "2020",
        "image": (io.BytesIO(_png_bytes()), "cover.png"),
    }, content_type="multipart/form-data")

    with app.app_context():
        ancien_nom = Livre.query.filter_by(titre="Livre Conserve").first().image_filename

    # Modifier sans fournir de nouvelle image
    client.post("/catalogue/Livre Conserve/modifier", data={
        "titre": "Livre Conserve",
        "auteur": "Autre Auteur",
        "annee_publication": "2022",
    }, follow_redirects=True)

    with app.app_context():
        livre = Livre.query.filter_by(titre="Livre Conserve").first()
        assert livre.image_filename == ancien_nom


# --- Suppression d'un livre supprime l'image ---

def test_supprimer_livre_supprime_image(app, client):
    _make_user(app, "user@test.com")
    _login(client, "user@test.com")
    client.post("/catalogue/ajouter", data={
        "titre": "Livre A Supprimer",
        "auteur": "Auteur",
        "annee_publication": "2020",
        "image": (io.BytesIO(_png_bytes()), "cover.png"),
    }, content_type="multipart/form-data")

    with app.app_context():
        livre = Livre.query.filter_by(titre="Livre A Supprimer").first()
        nom_image = livre.image_filename

    chemin = os.path.join(app.config["UPLOAD_FOLDER"], nom_image)
    assert os.path.isfile(chemin)

    client.post("/catalogue/Livre A Supprimer/supprimer", follow_redirects=True)

    assert not os.path.isfile(chemin)
    with app.app_context():
        assert Livre.query.filter_by(titre="Livre A Supprimer").first() is None


# --- image_filename dans le modèle ---

def test_image_filename_nullable(app):
    with app.app_context():
        livre = Livre(titre="Test", auteur="A", annee_publication=2000)
        db.session.add(livre)
        db.session.commit()
        assert livre.image_filename is None
