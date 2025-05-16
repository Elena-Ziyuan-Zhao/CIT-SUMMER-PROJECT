from db import db
from datetime import datetime
class Rating(db.Model):
    __tablename__ = "ratings" 

    id = db.mapped_column(db.Integer, primary_key = True)
    secret_id = db.mapped_column(db.ForeignKey("secrets.id"))
    # user_id = db.mapped_column(db.ForeignKey('users.id'))
    rating = db.mapped_column(db.Integer, default = 0)

    secret = db.relationship("Secret", back_populates= "ratings")
    # created_date = db.mapped_column(db.DateTime, default = datetime.now())
    