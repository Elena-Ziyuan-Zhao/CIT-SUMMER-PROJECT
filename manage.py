from db import db
from models import *
from app import app 
from sys import argv
from datetime import datetime, timedelta

def create_tables():
    db.create_all()


option = argv[1]
if __name__ == "__main__":
    app.app_context().push()
    if option == "create":
        create_tables()
        print("tables successfullt created")
    else:
        print("not defined yet")