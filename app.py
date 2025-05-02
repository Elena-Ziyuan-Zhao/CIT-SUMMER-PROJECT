from flask import Flask, render_template, redirect, url_for, request
from models import *
from db import db
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wall.db"
app.instance_path = Path("wall").resolve()
db.init_app(app)

# homepage
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/secrets")
def secrets():
    secrets = db.session.execute(db.select(Secret)).scalars()
    return render_template("all_secrets.html", secrets=secrets)

@app.route("/profile/<int:id>" )
def profile_detail(id):
    user = db.session.execute(db.select(User).where(User.id == id)).scalar()
    return render_template("profile.html", user=user)


@app.route("/profile/<int:id>/create", methods = ["POST", "GET"])
def create_secret(id):
    user =db.session.execute(db.select(User).where(User.id == id)).scalar()
    if request.method == "POST":
        content = request.form.get("content")
        title = request.form.get("title")
        new_secret = Secret(title = title, content = content, user = user)
        db.session.add(new_secret)
        db.session.commit()
        return redirect(url_for(f'profile_detail', id=user.id))
    else:
        return render_template("create.html", user=user)

# show single secret by id
@app.route("/secrets/<int:secret_id>")
def view_secret(secret_id):
    secret = Secret.query.get(secret_id)
    if not secret:
        return render_template("error.html", message="Secret not found"), 404
    return render_template("secret_detail.html", secret=secret)

if __name__ == "__main__":
    app.run(debug=True, port=8888)