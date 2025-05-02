from db import db
from models import *
from app import app
import csv
from sys import argv
from datetime import datetime, timedelta
import random

def create_tables():
    db.create_all()

def drop_tables():
    db.drop_all()


def import_data():
    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User()
            user.first_name = row["first_name"]
            user.second_name = row["second_name"]
            user.email = row["email"]
            user.username = row["username"]
            user.password = row["password"]
            db.session.add(user)
    db.session.commit()

def generate_secrets():
    with open("secrets.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            secret = Secret()
            secret.title = row["title"]
            secret.content = row["content"]
            random_user = db.session.execute(db.select(User).order_by(db.func.random())).scalar()
            secret.user = random_user
            db.session.add(secret)
    db.session.commit()            
            
    


option = argv[1]
if __name__ == "__main__":
    app.app_context().push()
    if option == "create":
        create_tables()
        print("tables successfully created")
    elif option == "drop":
        drop_tables()
        print("tables successfully droped")
    elif option == "import":
        import_data()
        generate_secrets()
        print("data successfully imported")
    else:
        print(f'{option} not defined')

