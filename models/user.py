from db import db
from datetime import datetime
class User(db.Model):
    __tablename__ = "users" 

    id = db.mapped_column(db.Integer, primary_key = True)
    first_name = db.mapped_column(db.String)
    second_name = db.mapped_column(db.String)
    username = db.mapped_column(db.String)
    user_type = db.mapped_column(db.String, default = "regular")
    email = db.mapped_column(db.String)
    password = db.mapped_column(db.String)
    created_date = db.mapped_column(db.DateTime, default = datetime.now())

    secrets = db.relationship("Secret", back_populates="user")
    # comments = db.relationship("Comment", back_populates="user")


    



