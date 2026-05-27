import logging
import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from models.livre import db

# Logging centralisé (CS06)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("the_library")


def create_app(config=None):
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///bibliotheque.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(32))
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads", "livres")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 Mo max avant compression

    if config:
        app.config.update(config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialisation de la base de données
    db.init_app(app)

    # Protection CSRF (CS05)
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Initialisation de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.utilisateur import User
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import jsonify
        return jsonify({"erreur": "Authentification requise"}), 401

    # Enregistrement des blueprints
    from routes.livres import livres_bp
    from routes.reservations import reservations_bp
    from routes.auth import auth_bp
    from routes.pages import pages_bp
    from routes.admin import admin_bp

    # Les routes API JSON sont exemptées du CSRF
    csrf.exempt(livres_bp)
    csrf.exempt(reservations_bp)
    csrf.exempt(auth_bp)

    app.register_blueprint(livres_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(admin_bp)

    # Headers de sécurité HTTP globaux (CS04) — couvre toutes les routes HTML et API
    @app.after_request
    def ajouter_headers_securite(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "img-src 'self' data:;"
        )
        return response

    # Gestionnaire d'erreur 413 : fichier trop volumineux
    @app.errorhandler(413)
    def fichier_trop_grand(e):
        from flask import flash, redirect, request, url_for
        flash("L'image dépasse la taille maximale autorisée (10 Mo).", "danger")
        referrer = request.referrer
        if referrer:
            return redirect(referrer)
        return redirect(url_for("pages.catalogue"))

    # Création des tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app = create_app()
    app.run(debug=debug)
