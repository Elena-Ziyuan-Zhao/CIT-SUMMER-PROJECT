from db import db
from datetime import datetime
import hashlib
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users" 

    id = db.mapped_column(db.Integer, primary_key = True)
    first_name = db.mapped_column(db.String)
    second_name = db.mapped_column(db.String)
    username = db.mapped_column(db.String)
    user_type = db.mapped_column(db.String, default = "regular")
    email = db.mapped_column(db.String)
    password = db.mapped_column(db.String)
    created_date = db.mapped_column(db.DateTime, default = datetime.now())
    
    secrets = db.relationship("Secret", back_populates="user", cascade="all, delete-orphan") 
    # Cascade Delete: when we delete a user, all their secrets are deleted too
    
    # comments = db.relationship("Comment", back_populates="user")


    def hash_passowrd(self, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        self.password = hashed
    
    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()



