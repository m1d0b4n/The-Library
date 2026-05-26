from flask import Flask
from models.livre import db


def create_app(config=None):
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bibliotheque.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "change-this-in-production"

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
    app = create_app()
    app.run(debug=True)
