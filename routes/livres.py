from flask import Blueprint, jsonify, request, abort
from models.livre import Livre, db

livres_bp = Blueprint("livres", __name__, url_prefix="/livres")

MAX_LENGTH = 200
ANNEE_MIN = 1000
ANNEE_MAX = 2100


def _valider_champs(titre, auteur, annee):
    """Valide les champs d'un livre. Lève ValueError si invalide (CS01)."""
    if not isinstance(titre, str) or not titre.strip():
        raise ValueError("Le titre est obligatoire et doit être une chaîne non vide.")
    if len(titre) > MAX_LENGTH:
        raise ValueError(f"Le titre ne doit pas dépasser {MAX_LENGTH} caractères.")
    if not isinstance(auteur, str) or not auteur.strip():
        raise ValueError("L'auteur est obligatoire et doit être une chaîne non vide.")
    if len(auteur) > MAX_LENGTH:
        raise ValueError(f"L'auteur ne doit pas dépasser {MAX_LENGTH} caractères.")
    if not isinstance(annee, int):
        raise ValueError("L'année de publication doit être un entier.")
    if not (ANNEE_MIN <= annee <= ANNEE_MAX):
        raise ValueError(f"L'année doit être comprise entre {ANNEE_MIN} et {ANNEE_MAX}.")


# Headers de sécurité gérés globalement dans app.py (after_request global)


@livres_bp.get("/")
def lister_livres():
    """F02 — Lister tous les livres."""
    livres = Livre.query.all()
    return jsonify([l.to_dict() for l in livres]), 200


@livres_bp.post("/")
def ajouter_livre():
    """F01 — Ajouter un livre."""
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Corps JSON manquant.")

    try:
        titre = data.get("titre", "")
        auteur = data.get("auteur", "")
        annee = data.get("annee_publication")
        _valider_champs(titre, auteur, annee)
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 422

    if Livre.query.filter_by(titre=titre.strip()).first():
        return jsonify({"erreur": "Un livre avec ce titre existe déjà."}), 409

    livre = Livre(
        titre=titre.strip(),
        auteur=auteur.strip(),
        annee_publication=annee,
    )
    db.session.add(livre)
    db.session.commit()
    return jsonify(livre.to_dict()), 201


@livres_bp.get("/<string:titre>")
def rechercher_livre(titre):
    """F03 — Rechercher un livre par titre."""
    livre = Livre.query.filter(
        Livre.titre.ilike(titre.strip())
    ).first_or_404(description=f"Livre '{titre}' introuvable.")
    return jsonify(livre.to_dict()), 200


@livres_bp.put("/<string:titre>")
def modifier_livre(titre):
    """F05 — Modifier un livre."""
    livre = Livre.query.filter(
        Livre.titre.ilike(titre.strip())
    ).first_or_404(description=f"Livre '{titre}' introuvable.")

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Corps JSON manquant.")

    nouveau_titre = data.get("titre", livre.titre)
    nouvel_auteur = data.get("auteur", livre.auteur)
    nouvelle_annee = data.get("annee_publication", livre.annee_publication)

    try:
        _valider_champs(nouveau_titre, nouvel_auteur, nouvelle_annee)
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 422

    livre.titre = nouveau_titre.strip()
    livre.auteur = nouvel_auteur.strip()
    livre.annee_publication = nouvelle_annee
    db.session.commit()
    return jsonify(livre.to_dict()), 200


@livres_bp.delete("/<string:titre>")
def supprimer_livre(titre):
    """F04 — Supprimer un livre."""
    livre = Livre.query.filter(
        Livre.titre.ilike(titre.strip())
    ).first_or_404(description=f"Livre '{titre}' introuvable.")
    db.session.delete(livre)
    db.session.commit()
    return jsonify({"message": f"'{livre.titre}' supprimé."}), 200

