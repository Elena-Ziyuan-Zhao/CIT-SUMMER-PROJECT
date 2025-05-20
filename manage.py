from db import db
from models import *
import csv
from sys import argv
from datetime import datetime, timedelta
import random
import os



def create_tables():
    db.create_all()



def import_data():
    csv_path = "/etc/secrets/students.csv"
    if not os.path.exists(csv_path):
        csv_path = "students.csv"
    with open(csv_path, "r", encoding="utf-8") as file:
        # read csv into dictionary
        # for example: {first_name: a, second_name: b}
        reader = csv.DictReader(file)
        for row in reader:
            student = Student(first_name = row["first_name"], second_name = row["second_name"], email = row["email"] )
            if row["role"] == "admin":
                user = User(first_name = row["first_name"], second_name = row["second_name"], email = row["email"], username = row["username"], user_type = row["role"])
                user.hash_passowrd(row["password"])
                db.session.add(user)
            db.session.add(student)
    db.session.commit()

def generate_secrets():
    with open("secrets.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            random_user = db.session.execute(db.select(User).order_by(db.func.random())).scalar()
            secret = Secret(title = row["title"], content = row["content"], user = random_user)
            db.session.add(secret)
    db.session.commit()


            

def drop_tables():
    db.drop_all()



'''
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

'''


def reset_db():
    drop_tables()
    create_tables()
    import_data()
    generate_secrets()
    