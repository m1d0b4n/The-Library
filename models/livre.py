from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Livre(db.Model):
    __tablename__ = "livres"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False, unique=True)
    auteur = db.Column(db.String(200), nullable=False)
    annee_publication = db.Column(db.Integer, nullable=False)
    disponible = db.Column(db.Boolean, default=True, nullable=False)
    reserve_par = db.Column(db.String(200), nullable=True, default=None)
    created_by = db.Column(db.String(200), nullable=True, default=None)
    image_filename = db.Column(db.String(300), nullable=True, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "auteur": self.auteur,
            "annee_publication": self.annee_publication,
            "disponible": self.disponible,
            "reserve_par": self.reserve_par,
        }
