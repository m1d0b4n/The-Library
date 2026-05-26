import logging
from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user
from models.livre import db, Livre
from models.utilisateur import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
logger = logging.getLogger("the_library.admin")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("pages.login"))
        if current_user.role != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@admin_required
def dashboard():
    nb_livres = Livre.query.count()
    nb_users = User.query.count()
    nb_reserves = Livre.query.filter_by(disponible=False).count()
    return render_template(
        "admin/dashboard.html",
        nb_livres=nb_livres,
        nb_users=nb_users,
        nb_reserves=nb_reserves,
    )


@admin_bp.route("/livres")
@admin_required
def livres():
    livres = Livre.query.order_by(Livre.titre).all()
    return render_template("admin/livres.html", livres=livres)


@admin_bp.route("/livres/<path:titre>/supprimer", methods=["POST"])
@admin_required
def supprimer_livre(titre):
    livre = Livre.query.filter_by(titre=titre).first_or_404()
    db.session.delete(livre)
    db.session.commit()
    logger.info("Admin %s a supprime le livre '%s'", current_user.email, titre)
    flash(f"Livre « {titre} » supprimé.", "success")
    return redirect(url_for("admin.livres"))


@admin_bp.route("/users")
@admin_required
def users():
    all_users = User.query.order_by(User.email).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if user.id == current_user.id:
        flash("Vous ne pouvez pas modifier votre propre rôle.", "error")
        return redirect(url_for("admin.users"))
    user.role = "user" if user.role == "admin" else "admin"
    db.session.commit()
    action = "promu admin" if user.role == "admin" else "rôle admin révoqué"
    logger.info("Admin %s : %s pour %s", current_user.email, action, user.email)
    flash(f"Rôle de {user.email} mis à jour.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/supprimer", methods=["POST"])
@admin_required
def supprimer_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if user.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "error")
        return redirect(url_for("admin.users"))
    email = user.email
    db.session.delete(user)
    db.session.commit()
    logger.info("Admin %s a supprime l'utilisateur %s", current_user.email, email)
    flash(f"Utilisateur {email} supprimé.", "success")
    return redirect(url_for("admin.users"))
