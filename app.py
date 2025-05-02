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

# show all secrets
@app.route("/all-secrets")
def all_secrets():
    secrets = Secret.query.order_by(Secret.created_date.desc()).all()
    return render_template("all_secrets.html", secrets=secrets)

# show single secret by id
@app.route("/secret/<int:secret_id>")
def view_secret(secret_id):
    secret = Secret.query.get(secret_id)
    if not secret:
        return render_template("error.html", message="Secret not found"), 404
    return render_template("secret_detail.html", secret=secret)

if __name__ == "__main__":
    app.run(debug=True, port=8888)