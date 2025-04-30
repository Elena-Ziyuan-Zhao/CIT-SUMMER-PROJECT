from db import db
from datetime import datetime
class User(db.Model):
    __tablename__ = "users" 

    id = db.mapped_column(db.Integer, primary_key = True)
    first_name = db.mapped_column(db.String)
    second_name = db.mapped_column(db.String)
    anonymous_name = db.mapped_column(db.String, default = None)
    user_type = db.mapped_column(db.String, default = "regular")
    email = db.mapped_column(db.String)
    password = db.mapped_column(db.String)

    created_date = db.mapped_column(db.DateTime, default = datetime.now())

    secretes = db.relationship("Secrete", back_populates="")



    



