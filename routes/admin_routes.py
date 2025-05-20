from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from models.secret import Secret
from db import db
from flask_login import current_user, login_required
from sqlalchemy import or_, func

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
def admin_dashboard():


    users = db.session.execute(db.select(User)).scalars()
    secrets = db.session.execute(db.select(Secret)).scalars()

    return render_template("admin.html", current_user = current_user)
 

# manage users

@admin_bp.route("/users")
@login_required
def admin_users():
    query = request.args.get("q", "").strip()
    stmt = db.select(User)
    if query:
        if query.isdigit():
            # if only digits, assume it's a user ID
            stmt = stmt.where(User.id == int(query))
        else:
            stmt = stmt.where(
                User.email.contains(query)
            )
    users = db.session.execute(stmt).scalars()
    return render_template("admin_users.html", users=users, query=query)

@admin_bp.route("/user/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("admin.admin_users"))


# manage secrets

@admin_bp.route("/secrets")
@login_required
def admin_secrets():
    query = request.args.get("q", "").strip().lower()
    stmt = db.select(Secret).join(Secret.user, isouter=True)

    if query:
        query_like = f"%{query}%"
        if query.isdigit():
            stmt = stmt.where(
                (Secret.user_id == int(query)) |
                func.lower(Secret.title).like(query_like)
            )
        else:
            stmt = stmt.where(
                or_(
                    func.lower(Secret.title).like(query_like),
                    func.lower(User.email).like(query_like)
                )
            )

    secrets = db.session.execute(stmt).scalars()
    return render_template("admin_secrets.html", secrets=secrets, query=query)

@admin_bp.route("/secret/<int:secret_id>/delete", methods=["POST"])
@login_required
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
@login_required
def admin_secret_detail(secret_id):
    secret = db.session.execute(
        db.select(Secret).where(Secret.id == secret_id)
    ).scalar()
    if not secret:
        return render_template("error.html", message="Secret not found"), 404
    return render_template("admin_secret_detail.html", secret=secret)