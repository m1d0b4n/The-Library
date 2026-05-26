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

    if config:
        app.config.update(config)

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

    # Les routes API JSON sont exemptées du CSRF
    csrf.exempt(livres_bp)
    csrf.exempt(reservations_bp)
    csrf.exempt(auth_bp)

    app.register_blueprint(livres_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    # Création des tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app = create_app()
    app.run(debug=debug)
