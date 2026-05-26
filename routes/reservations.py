from flask import Blueprint, jsonify, request
from models.livre import Livre, db

reservations_bp = Blueprint("reservations", __name__, url_prefix="/livres")


@reservations_bp.post("/<string:titre>/reserver")
def reserver_livre(titre):
    """F06 — Réserver un livre si disponible."""
    livre = Livre.query.filter(
        Livre.titre.ilike(titre.strip())
    ).first_or_404(description=f"Livre '{titre}' introuvable.")

    if not livre.disponible:
        return jsonify({
            "erreur": f"'{livre.titre}' est déjà réservé par {livre.reserve_par}."
        }), 409

    data = request.get_json(silent=True) or {}
    reserve_par = data.get("reserve_par", "").strip()
    if not reserve_par:
        return jsonify({"erreur": "Le champ 'reserve_par' est obligatoire."}), 422

    if len(reserve_par) > 200:
        return jsonify({"erreur": "'reserve_par' ne doit pas dépasser 200 caractères."}), 422

    livre.disponible = False
    livre.reserve_par = reserve_par
    db.session.commit()
    return jsonify(livre.to_dict()), 200


@reservations_bp.post("/<string:titre>/annuler")
def annuler_reservation(titre):
    """F07 — Annuler la réservation d'un livre."""
    livre = Livre.query.filter(
        Livre.titre.ilike(titre.strip())
    ).first_or_404(description=f"Livre '{titre}' introuvable.")

    if livre.disponible:
        return jsonify({"erreur": f"'{livre.titre}' n'est pas réservé."}), 409

    livre.disponible = True
    livre.reserve_par = None
    db.session.commit()
    return jsonify(livre.to_dict()), 200
