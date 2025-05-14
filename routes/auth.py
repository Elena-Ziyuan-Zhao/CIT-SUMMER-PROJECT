from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from db import db
from models import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ["GET"])
def get_login():
    return render_template('login.html')

@auth.route('/login', methods = ["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('home'))
    else:
        flash("Invalid email or password")
        return redirect(url_for('auth.get_login'))


@auth.route('/register')
def get_register():
    return render_template("register.html")

@auth.route('register', methods = ["POST"])
def register():
    email = request.form["email"]
    password = request.form['password']
    confirm = request.form['confirm']
    first_name = request.form['first_name']
    second_name = request.form['second_name']
    username = request.form['username']
    
    find_user = db.session.execute(db.select(User).where(User.email == email)).scalar()

    if password != confirm:
        flash("Password does not match")
    elif find_user:
        flash("This email is already registered")
    else:
        user = User(email=email,
                first_name=first_name,
                second_name=second_name,
                username = username)
        user.hash_passowrd(password)
        db.session.add(user)
        db.session.commit()
        flash("registration successful")
        return redirect(url_for("auth.get_login"))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
