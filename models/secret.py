from db import db
from datetime import datetime
class Secret(db.Model):
    __tablename__ = "secrets" 

    id = db.mapped_column(db.Integer, primary_key = True)
    title = db.mapped_column(db.String)
    content = db.mapped_column(db.String)
    created_date = db.mapped_column(db.DateTime, default = datetime.now())

    user_id = db.mapped_column(db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="secrets")
