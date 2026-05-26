from flask import Flask
from models.livre import db
import os


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

    # Enregistrement des blueprints
    from routes.livres import livres_bp
    from routes.reservations import reservations_bp

    app.register_blueprint(livres_bp)
    app.register_blueprint(reservations_bp)

    # Création des tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app = create_app()
    app.run(debug=debug)
