import io
import logging
import os
import uuid
from datetime import date

import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
from werkzeug.utils import secure_filename
from models.livre import db
from models.utilisateur import User
from models.livre import Livre

pages_bp = Blueprint("pages", __name__)
logger = logging.getLogger("the_library.pages")

EXTENSIONS_AUTORISEES = {"jpg", "jpeg", "png", "webp", "gif"}

_MAGIC = [
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "jpeg"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"RIFF", "webp"),  # vérifié plus loin
]


def _detecter_mime(data: bytes) -> str | None:
    """Détecte le type d'image à partir des magic bytes."""
    for magic, mime in _MAGIC:
        if data[:len(magic)] == magic:
            if mime == "webp" and data[8:12] != b"WEBP":
                return None
            return mime
    return None


# Taille cible après compression (en octets)
_TAILLE_MAX_FINALE = 500 * 1024  # 500 Ko
_DIMENSION_MAX = 1200  # px (côté le plus long)


def _compresser_image(data: bytes, ext: str) -> bytes:
    """Redimensionne et compresse l'image pour qu'elle reste sous 500 Ko."""
    try:
        buf_in = io.BytesIO(data)
        img = Image.open(buf_in)
        img.load()  # force le chargement avant que le BytesIO soit perdu
    except Exception:
        # Si Pillow ne peut pas décoder, on retourne les données brutes telles quelles
        return data

    # Conversion RGBA/P → RGB pour JPEG (pas d'alpha en JPEG)
    format_pil = "WEBP" if ext == "webp" else ("PNG" if ext == "png" else ("GIF" if ext == "gif" else "JPEG"))
    if format_pil == "JPEG" and img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")

    # Redimensionnement si nécessaire
    w, h = img.size
    if max(w, h) > _DIMENSION_MAX:
        ratio = _DIMENSION_MAX / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    # Compression itérative pour JPEG/WEBP
    if format_pil in ("JPEG", "WEBP"):
        qualite = 85
        while qualite >= 40:
            buf = io.BytesIO()
            img.save(buf, format=format_pil, quality=qualite, optimize=True)
            if buf.tell() <= _TAILLE_MAX_FINALE:
                break
            qualite -= 10
        return buf.getvalue()

    # PNG / GIF : compression sans perte de qualité
    buf = io.BytesIO()
    img.save(buf, format=format_pil, optimize=True)
    return buf.getvalue()


def _sauvegarder_image(fichier):
    """Valide, compresse et sauvegarde une image uploadée. Renvoie le nom du fichier ou None si absent."""
    if not fichier or fichier.filename == "":
        return None

    ext = fichier.filename.rsplit(".", 1)[-1].lower() if "." in fichier.filename else ""
    if ext not in EXTENSIONS_AUTORISEES:
        raise ValueError("Format non autorisé (JPG, PNG, WEBP, GIF uniquement).")

    data = fichier.read()
    mime = _detecter_mime(data)
    if mime is None:
        raise ValueError("Le fichier n'est pas une image valide.")

    data = _compresser_image(data, ext)

    nom = f"{uuid.uuid4().hex}.{ext}"
    chemin = os.path.join(current_app.config["UPLOAD_FOLDER"], nom)
    with open(chemin, "wb") as f:
        f.write(data)
    return nom


# --- Accueil ---

@pages_bp.route("/")
def index():
    from models.utilisateur import User
    setup_needed = User.query.count() == 0
    return render_template("index.html", setup_needed=setup_needed)


@pages_bp.route("/setup", methods=["POST"])
def setup():
    if User.query.count() > 0:
        from flask import abort
        abort(403)
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not email or len(email) > 200:
        flash("Email invalide.", "error")
        return redirect(url_for("pages.index"))
    if len(password) < 8:
        flash("Mot de passe trop court (min. 8 caractères).", "error")
        return redirect(url_for("pages.index"))
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    admin = User(email=email, password_hash=password_hash, role="admin")
    db.session.add(admin)
    db.session.commit()
    login_user(admin)
    logger.info("Setup initial : admin cree %s (IP: %s)", email, request.remote_addr)
    flash(f"Bienvenue ! Compte admin créé pour {email}.", "success")
    return redirect(url_for("admin.dashboard"))


# --- Auth ---

@pages_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("pages.liste_livres"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            login_user(user)
            logger.info("Connexion reussie : %s (IP: %s)", email, request.remote_addr)
            return redirect(url_for("pages.liste_livres"))
        logger.warning("Echec connexion : %s (IP: %s)", email, request.remote_addr)
        flash("Email ou mot de passe incorrect.", "error")
    return render_template("auth/login.html")


@pages_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("pages.liste_livres"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email or len(email) > 200:
            flash("Email invalide.", "error")
        elif len(password) < 8:
            flash("Mot de passe trop court (min. 8 caractères).", "error")
        elif User.query.filter_by(email=email).first():
            flash("Email déjà utilisé.", "error")
        else:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            db.session.add(User(email=email, password_hash=password_hash))
            db.session.commit()
            logger.info("Inscription : %s (IP: %s)", email, request.remote_addr)
            flash("Compte créé ! Connectez-vous.", "success")
            return redirect(url_for("pages.login"))
    return render_template("auth/register.html")


@pages_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logger.info("Deconnexion : %s", current_user.email)
    logout_user()
    flash("Vous êtes déconnecté.", "success")
    return redirect(url_for("pages.index"))


# --- Livres ---

@pages_bp.route("/catalogue")
def liste_livres():
    livres = Livre.query.order_by(Livre.titre).all()
    return render_template("livres/index.html", livres=livres)


@pages_bp.route("/catalogue/<path:titre>")
def detail_livre(titre):
    livre = Livre.query.filter_by(titre=titre).first_or_404()
    return render_template("livres/detail.html", livre=livre)


@pages_bp.route("/catalogue/ajouter", methods=["GET", "POST"])
@login_required
def ajouter_livre():
    today = date.today().isoformat()
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        auteur = request.form.get("auteur", "").strip()
        date_pub = request.form.get("annee_publication", "").strip()
        try:
            if not date_pub:
                raise ValueError
            annee = int(date_pub.split("-")[0])
        except (ValueError, IndexError):
            flash("Date de publication invalide.", "error")
            return render_template("livres/form.html", livre=None, today=today)

        if not titre or len(titre) > 200 or not auteur or len(auteur) > 200:
            flash("Titre et auteur requis (max 200 caractères).", "error")
        elif annee < 1000 or annee > date.today().year:
            flash(f"Année hors limites (1000-{date.today().year}).", "error")
        elif Livre.query.filter_by(titre=titre).first():
            flash("Un livre avec ce titre existe déjà.", "error")
        else:
            try:
                image_filename = _sauvegarder_image(request.files.get("image"))
            except ValueError as e:
                flash(str(e), "error")
                return render_template("livres/form.html", livre=None, today=today)
            db.session.add(Livre(
                titre=titre, auteur=auteur, annee_publication=annee,
                created_by=current_user.email, image_filename=image_filename
            ))
            db.session.commit()
            flash(f"« {titre} » ajouté avec succès.", "success")
            return redirect(url_for("pages.liste_livres"))
    return render_template("livres/form.html", livre=None, today=today)


@pages_bp.route("/catalogue/<path:titre>/modifier", methods=["GET", "POST"])
@login_required
def modifier_livre(titre):
    livre = Livre.query.filter_by(titre=titre).first_or_404()
    if not livre.disponible:
        flash("Impossible de modifier un livre réservé.", "error")
        return redirect(url_for("pages.detail_livre", titre=titre))
    if livre.created_by and livre.created_by != current_user.email:
        flash("Vous ne pouvez pas modifier un livre qui ne vous appartient pas.", "error")
        return redirect(url_for("pages.detail_livre", titre=titre))
    today = date.today().isoformat()
    if request.method == "POST":
        auteur = request.form.get("auteur", "").strip()
        date_pub = request.form.get("annee_publication", "").strip()
        try:
            if not date_pub:
                raise ValueError
            annee = int(date_pub.split("-")[0])
        except (ValueError, IndexError):
            flash("Date de publication invalide.", "error")
            return render_template("livres/form.html", livre=livre, today=today)

        if not auteur or len(auteur) > 200:
            flash("Auteur requis (max 200 caractères).", "error")
        elif annee < 1000 or annee > date.today().year:
            flash(f"Année hors limites (1000-{date.today().year}).", "error")
        else:
            try:
                nouvelle_image = _sauvegarder_image(request.files.get("image"))
            except ValueError as e:
                flash(str(e), "error")
                return render_template("livres/form.html", livre=livre, today=today)
            livre.auteur = auteur
            livre.annee_publication = annee
            if nouvelle_image:
                # Supprimer l'ancienne image si elle existe
                if livre.image_filename:
                    ancien = os.path.join(current_app.config["UPLOAD_FOLDER"], livre.image_filename)
                    if os.path.isfile(ancien):
                        os.remove(ancien)
                livre.image_filename = nouvelle_image
            db.session.commit()
            flash("Livre modifié.", "success")
            return redirect(url_for("pages.detail_livre", titre=livre.titre))
    return render_template("livres/form.html", livre=livre, today=today)


@pages_bp.route("/catalogue/<path:titre>/supprimer", methods=["POST"])
@login_required
def supprimer_livre(titre):
    livre = Livre.query.filter_by(titre=titre).first_or_404()
    if not livre.disponible:
        flash("Impossible de supprimer un livre réservé.", "error")
        return redirect(url_for("pages.detail_livre", titre=titre))
    if livre.created_by and livre.created_by != current_user.email:
        flash("Vous ne pouvez pas supprimer un livre qui ne vous appartient pas.", "error")
        return redirect(url_for("pages.detail_livre", titre=titre))
    if livre.image_filename:
        chemin = os.path.join(current_app.config["UPLOAD_FOLDER"], livre.image_filename)
        if os.path.isfile(chemin):
            os.remove(chemin)
    db.session.delete(livre)
    db.session.commit()
    logger.warning("Suppression livre : '%s' par %s", titre, current_user.email)
    flash(f"« {titre} » supprimé.", "success")
    return redirect(url_for("pages.liste_livres"))


@pages_bp.route("/catalogue/<path:titre>/reserver", methods=["POST"])
@login_required
def reserver(titre):
    livre = Livre.query.filter_by(titre=titre).first_or_404()
    if not livre.disponible:
        flash("Ce livre est déjà réservé.", "error")
    else:
        livre.disponible = False
        livre.reserve_par = current_user.email
        db.session.commit()
        logger.info("Reservation : '%s' par %s", titre, current_user.email)
        flash(f"« {titre} » réservé.", "success")
    return redirect(url_for("pages.detail_livre", titre=titre))


@pages_bp.route("/catalogue/<path:titre>/annuler", methods=["POST"])
@login_required
def annuler(titre):
    livre = Livre.query.filter_by(titre=titre).first_or_404()
    if livre.disponible or livre.reserve_par != current_user.email:
        flash("Vous ne pouvez pas annuler cette réservation.", "error")
    else:
        livre.disponible = True
        livre.reserve_par = None
        db.session.commit()
        flash(f"Réservation de « {titre} » annulée.", "success")
    return redirect(url_for("pages.detail_livre", titre=titre))
