from db import db
from datetime import datetime
class Comment(db.Model):
    __tablename__ = "comments" 

    id = db.mapped_column(db.Integer, primary_key = True)
    comment = db.mapped_column(db.String)
    
    user_id = db.mapped_column(db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="comments")
    
    secret_id = db.mapped_column(db.ForeignKey("secrets.id"))
    secret = db.relationship("Secret", back_populates="comments")

    commented_at = db.mapped_column(db.DateTime, default = datetime.now())

