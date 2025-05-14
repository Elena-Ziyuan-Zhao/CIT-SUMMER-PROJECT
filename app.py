from flask import Flask, render_template, redirect, url_for, request
from models import *
from db import db
from pathlib import Path
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from routes import register_routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wall.db"
app.instance_path = Path("wall").resolve()
db.init_app(app)

register_routes(app)

scheduler = BackgroundScheduler()

def delete_expired_secrets():

    with app.app_context():
        now = datetime.now()
        expired_secrets = db.session.execute(db.select(Secret).where(Secret.expires_at < now)).scalars()
        for secret in expired_secrets:
            print(f"Deleted {secret.title}")
            db.session.delete(secret)
        db.session.commit()
    
scheduler.add_job(delete_expired_secrets, 'interval', seconds=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/secrets")
def secrets():
    sort = request.args.get("sort")
    if sort == "spicy":
        secrets = db.session.execute(db.select(Secret).order_by(Secret.rating.desc())).scalars()
    else:
        secrets = db.session.execute(db.select(Secret)).scalars()
    return render_template("all_secrets.html", secrets=secrets)


# show single secret by id
@app.route("/secrets/<int:id>", methods=["GET"])
def secret_detail(id):
    secret = db.session.execute(db.select(Secret).where(Secret.id == id)).scalar()
    if not secret:
        return render_template("error.html", message="Secret not found"), 404
    return render_template("secret_detail.html", secret=secret)

@app.route("/secrets/<int:id>", methods=["POST"])
def react_secret(id):
    secret = db.session.execute(db.select(Secret).where(Secret.id == id)).scalar()
    if not secret:
        return render_template("error.html", message="Secret not found"), 404
    comment = request.form.get("comment")
    if comment:
        new_comment = Comment(secret = secret, comment = comment)
        db.session.add(new_comment)
        db.session.commit()
    rating = request.form.get("rating")
    if rating:
        rating = int(rating)
        new_rate = Rating(rating = rating, secret = secret)
        secret.rating += rating
        db.session.add(new_rate)
        db.session.commit()
    return render_template("secret_detail.html", secret=secret)

@app.route("/profile/<int:id>", methods = ["GET"])
def profile_detail(id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()
    return render_template("profile.html", user=user)

@app.route("/secret/<int:id>/delete", methods = ["POST"])
def delete_secret(id):
    secret = db.session.execute(db.select(Secret).where(Secret.id == id)).scalar()
    db.session.delete(secret)
    db.session.commit()
    return redirect(url_for('profile_detail', id = secret.user_id))

@app.route("/secret/<int:id>/edit", methods = ["POST", "GET"])
def edit_secret(id):
    secret = db.session.execute(db.select(Secret).where(Secret.id == id)).scalar()
    if request.method == "GET":
        return render_template("edit_secrets.html", secret = secret)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        secret.title = title
        secret.content = content
        db.session.commit()
        return redirect(url_for("profile_detail", id = secret.user_id))


@app.route("/profile/<int:id>/create", methods = ["POST", "GET"])
def create_secret(id):
    user =db.session.execute(db.select(User).where(User.id == id)).scalar()
    if request.method == "POST":
        content = request.form.get("content")
        title = request.form.get("title")
        hours = request.form.get("hour")
        minutes = request.form.get("minutes")
        total_minutes = 0
        if hours:
            total_minutes += int(hours) * 60
        if minutes:
            total_minutes += int(minutes)
        
        if 0 < total_minutes <= 2800:
            expires_at = datetime.now() + timedelta(minutes=total_minutes)
            new_secret = Secret(title = title, content = content, user = user, expires_at = expires_at, created_date = datetime.now())
        else:
            new_secret = Secret(title = title, content = content, user = user)
        db.session.add(new_secret)
        db.session.commit()
        return redirect(url_for('profile_detail', id=user.id))
    else:
        return render_template("create_secrets.html", user=user)


if __name__ == "__main__":
    app.run(debug=True, port=8888)