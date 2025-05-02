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
    user = db.relationship("User", back_populates="secrets")

    @property
    def anonymous_poster(self):
        with open("fakenames.csv", "r") as file:
            fakenames = [line.strip() for line in file][1:]
        return random.choice(fakenames)
        
            