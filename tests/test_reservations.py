import pytest
from app import create_app
from models.livre import db as _db, Livre


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


@pytest.fixture
def livre_existant(app):
    """Insère un livre disponible en base pour les tests."""
    with app.app_context():
        livre = Livre(titre="Dune", auteur="Frank Herbert", annee_publication=1965)
        _db.session.add(livre)
        _db.session.commit()


# --- Tests réservation ---

def test_reserver_livre(client, livre_existant):
    """Réserver un livre disponible retourne 200 et disponible=False."""
    r = client.post("/livres/Dune/reserver", json={"reserve_par": "Alice"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["disponible"] is False
    assert data["reserve_par"] == "Alice"


def test_reserver_livre_deja_reserve(client, livre_existant):
    """Réserver un livre déjà réservé retourne 409."""
    client.post("/livres/Dune/reserver", json={"reserve_par": "Alice"})
    r = client.post("/livres/Dune/reserver", json={"reserve_par": "Bob"})
    assert r.status_code == 409


def test_reserver_sans_reserve_par(client, livre_existant):
    """Réserver sans 'reserve_par' retourne 422."""
    r = client.post("/livres/Dune/reserver", json={})
    assert r.status_code == 422


def test_reserver_livre_inexistant(client):
    """Réserver un livre inexistant retourne 404."""
    r = client.post("/livres/Inexistant/reserver", json={"reserve_par": "Alice"})
    assert r.status_code == 404


# --- Tests annulation ---

def test_annuler_reservation(client, livre_existant):
    """Annuler une réservation remet disponible=True et reserve_par=None."""
    client.post("/livres/Dune/reserver", json={"reserve_par": "Alice"})
    r = client.post("/livres/Dune/annuler")
    assert r.status_code == 200
    data = r.get_json()
    assert data["disponible"] is True
    assert data["reserve_par"] is None


def test_annuler_livre_non_reserve(client, livre_existant):
    """Annuler un livre non réservé retourne 409."""
    r = client.post("/livres/Dune/annuler")
    assert r.status_code == 409


def test_annuler_livre_inexistant(client):
    """Annuler la réservation d'un livre inexistant retourne 404."""
    r = client.post("/livres/Inexistant/annuler")
    assert r.status_code == 404


def test_reserver_puis_rerserver_apres_annulation(client, livre_existant):
    """Après annulation, un autre utilisateur peut réserver."""
    client.post("/livres/Dune/reserver", json={"reserve_par": "Alice"})
    client.post("/livres/Dune/annuler")
    r = client.post("/livres/Dune/reserver", json={"reserve_par": "Bob"})
    assert r.status_code == 200
    assert r.get_json()["reserve_par"] == "Bob"
