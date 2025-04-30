from db import db
from models import *
from app import app 
from sys import argv
from datetime import datetime, timedelta

def create_tables():
    db.create_all()

def drop_tables():
    db.drop_all()


option = argv[1]
if __name__ == "__main__":
    app.app_context().push()
    if option == "create":
        create_tables()
        print("tables successfullt created")
    elif option == "drop":
        drop_tables()
        print("successfully deleted")
    else:
        print("not defined yet")