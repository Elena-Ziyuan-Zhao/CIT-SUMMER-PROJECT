from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from db import db
from models import *
from datetime import datetime

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
        if user.user_type == "admin":
            return redirect(url_for("admin.admin_dashboard"))
        return redirect(url_for('home'))
    elif not user:
        flash("You are not a member")
    elif not user.check_password(password):
        flash("Incorrect password")
    return redirect(url_for('auth.get_login'))

@auth.route('/register')
def get_register():
    return render_template("register.html")

@auth.route('register', methods = ["POST"])
def register():
    email = request.form["email"]
    password = request.form['password']
    confirm = request.form['confirm']

    username = request.form['username']
    
    student = db.session.execute(db.select(Student).where(Student.email == email)).scalar()
    find_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    

    if password == confirm and not find_user and student:
        user = User(email=email,
                username = username,
                first_name = student.first_name,
                second_name = student.second_name,
                created_date = datetime.now())
        user.hash_passowrd(password)
        db.session.add(user)
        db.session.commit()
        flash("registration successful")
        return redirect(url_for("auth.get_login"))
    if password != confirm:
        flash("Password does not match")
    elif find_user:
        flash("This email is already registered")
    elif not student:
        flash("use your BCIT email")
    return redirect(url_for("auth.get_register"))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
