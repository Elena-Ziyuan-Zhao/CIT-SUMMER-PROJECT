from db import db
from datetime import datetime
class Comment(db.Model):
    __tablename__ = "comments" 
    id = db.mapped_column(db.Integer, primary_key = True)
    user_id = db.mapped_column(db.ForeignKey("users.id"))

    title = db.mapped_column(db.String)
    content = db.mapped_column(db.String)
    created_date = db.mapped_column(db.DateTime, default = datetime.now())

    secret_id = db.mapped_column(db.Integer, db.ForeignKey("secrets.id"))
    secret = db.relationship("Secret", back_populates="comments")
    

