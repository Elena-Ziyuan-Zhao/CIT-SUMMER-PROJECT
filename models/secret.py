from db import db
from datetime import datetime
import random

class Secret(db.Model):
    __tablename__ = "secrets" 

    id = db.mapped_column(db.Integer, primary_key = True)
    title = db.mapped_column(db.String)
    content = db.mapped_column(db.String)
    created_date = db.mapped_column(db.DateTime, default = datetime.now())
    user_id = db.mapped_column(db.ForeignKey("users.id"))
    expires_at = db.mapped_column(db.DateTime, default = None)
    
    user = db.relationship("User", back_populates="secrets")
    comments = db.relationship("Comment", back_populates="secret")

    rating = db.mapped_column(db.Integer, default = 0)
    ratings = db.relationship("Rating", back_populates = "secret")

    @property
    def anonymous_poster(self):
        with open("fakenames.csv", "r") as file:
            fakenames = [line.strip() for line in file][1:]
        return random.choice(fakenames)
