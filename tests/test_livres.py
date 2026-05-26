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


# --- Tests happy path ---

def test_lister_livres_vide(client):
    """GET /livres/ retourne une liste vide au départ."""
    r = client.get("/livres/")
    assert r.status_code == 200
    assert r.get_json() == []


def test_ajouter_livre(client):
    """POST /livres/ crée un livre et retourne 201."""
    r = client.post("/livres/", json={
        "titre": "Le Petit Prince",
        "auteur": "Saint-Exupéry",
        "annee_publication": 1943,
    })
    assert r.status_code == 201
    data = r.get_json()
    assert data["titre"] == "Le Petit Prince"
    assert data["disponible"] is True


def test_lister_livres_apres_ajout(client):
    """GET /livres/ retourne les livres ajoutés."""
    client.post("/livres/", json={"titre": "Dune", "auteur": "Herbert", "annee_publication": 1965})
    r = client.get("/livres/")
    assert r.status_code == 200
    assert len(r.get_json()) == 1


def test_rechercher_livre(client):
    """GET /livres/<titre> retourne le livre correspondant."""
    client.post("/livres/", json={"titre": "1984", "auteur": "Orwell", "annee_publication": 1949})
    r = client.get("/livres/1984")
    assert r.status_code == 200
    assert r.get_json()["auteur"] == "Orwell"


def test_modifier_livre(client):
    """PUT /livres/<titre> modifie les informations."""
    client.post("/livres/", json={"titre": "Dune", "auteur": "Herbert", "annee_publication": 1965})
    r = client.put("/livres/Dune", json={"auteur": "Frank Herbert"})
    assert r.status_code == 200
    assert r.get_json()["auteur"] == "Frank Herbert"


def test_supprimer_livre(client):
    """DELETE /livres/<titre> supprime le livre."""
    client.post("/livres/", json={"titre": "Dune", "auteur": "Herbert", "annee_publication": 1965})
    r = client.delete("/livres/Dune")
    assert r.status_code == 200
    assert client.get("/livres/Dune").status_code == 404


# --- Tests validation (CS01) ---

def test_ajouter_titre_vide(client):
    """Un titre vide est rejeté avec 422."""
    r = client.post("/livres/", json={"titre": "", "auteur": "X", "annee_publication": 2000})
    assert r.status_code == 422


def test_ajouter_titre_manquant(client):
    """Un titre absent est rejeté avec 422."""
    r = client.post("/livres/", json={"auteur": "X", "annee_publication": 2000})
    assert r.status_code == 422


def test_ajouter_annee_invalide(client):
    """Une année sous forme de chaîne est rejetée avec 422."""
    r = client.post("/livres/", json={"titre": "Test", "auteur": "X", "annee_publication": "deux mille"})
    assert r.status_code == 422


def test_ajouter_doublon(client):
    """Ajouter deux livres avec le même titre retourne 409."""
    payload = {"titre": "Dune", "auteur": "Herbert", "annee_publication": 1965}
    client.post("/livres/", json=payload)
    r = client.post("/livres/", json=payload)
    assert r.status_code == 409


def test_rechercher_livre_inexistant(client):
    """GET /livres/<titre> retourne 404 si le livre n'existe pas."""
    r = client.get("/livres/Inexistant")
    assert r.status_code == 404


# --- Tests sécurité XSS (CS04) ---

def test_headers_securite_presents(client):
    """Les headers de sécurité HTTP sont présents dans les réponses."""
    r = client.get("/livres/")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in r.headers


def test_xss_titre_echappe(client):
    """Un titre avec balise script est stocké et retourné échappé (pas exécuté)."""
    payload_xss = "<script>alert('xss')</script>"
    r = client.post("/livres/", json={
        "titre": payload_xss,
        "auteur": "Hacker",
        "annee_publication": 2024,
    })
    assert r.status_code == 201
    data = r.get_json()
    # Le titre est retourné tel quel en JSON (pas interprété comme HTML)
    assert data["titre"] == payload_xss
