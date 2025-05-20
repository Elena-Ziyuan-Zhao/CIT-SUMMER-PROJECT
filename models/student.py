from db import db
class Student(db.Model):
    __tablename__ = "students" 

    id = db.mapped_column(db.Integer, primary_key = True)
    first_name = db.mapped_column(db.String)
    second_name = db.mapped_column(db.String)
    email = db.mapped_column(db.String)