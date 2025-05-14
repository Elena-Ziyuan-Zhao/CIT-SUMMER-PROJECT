from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from models.secret import Secret
from db import db
from flask_login import current_user

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def admin_dashboard():


    users = db.session.execute(db.select(User)).scalars()
    secrets = db.session.execute(db.select(Secret)).scalars()

    return render_template("admin.html", current_user = current_user)
 

# manage users

@admin_bp.route("/users")
def admin_users():
    users = db.session.execute(db.select(User)).scalars()
    return render_template("admin_users.html", users=users)

@admin_bp.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("admin.admin_users"))

@admin_bp.route("/user/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    if user:
        user.username = request.form.get("name")
        db.session.commit()
    return redirect(url_for("admin.admin_users"))

# manage secrets

@admin_bp.route("/secrets")
def admin_secrets():
    secrets = db.session.execute(db.select(Secret)).scalars()
    return render_template("admin_secrets.html", secrets=secrets)

@admin_bp.route("/secret/<int:secret_id>/delete", methods=["POST"])
def admin_delete_secret(secret_id):
    secret = db.session.execute(
        db.select(Secret).where(Secret.id == secret_id)
    ).scalar()
    if secret:
        db.session.delete(secret)
        db.session.commit()
    return redirect(url_for("admin.admin_secrets"))

# read-only secret detail
@admin_bp.route("/secret/<int:secret_id>")
def admin_secret_detail(secret_id):
    secret = db.session.execute(
        db.select(Secret).where(Secret.id == secret_id)
    ).scalar()
    if not secret:
        return render_template("error.html", message="Secret not found"), 404
    return render_template("admin_secret_detail.html", secret=secret)