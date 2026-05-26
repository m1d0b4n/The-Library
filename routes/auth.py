import bcrypt
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.livre import db
from models.utilisateur import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

EMAIL_MAX = 200
PASSWORD_MIN = 8
PASSWORD_MAX = 200


def _erreur(message, code):
    return jsonify({"erreur": message}), code


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data:
        return _erreur("Corps JSON requis", 400)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or len(email) > EMAIL_MAX:
        return _erreur("Email invalide ou trop long (max 200 caractères)", 422)
    if not password or len(password) < PASSWORD_MIN:
        return _erreur(f"Mot de passe trop court (min {PASSWORD_MIN} caractères)", 422)
    if len(password) > PASSWORD_MAX:
        return _erreur("Mot de passe trop long (max 200 caractères)", 422)

    if User.query.filter_by(email=email).first():
        return _erreur("Email déjà utilisé", 409)

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return _erreur("Corps JSON requis", 400)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return _erreur("Email ou mot de passe incorrect", 401)

    login_user(user)
    return jsonify(user.to_dict()), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Déconnecté"}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify(current_user.to_dict()), 200
