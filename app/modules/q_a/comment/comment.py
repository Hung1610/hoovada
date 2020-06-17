from datetime import datetime

from app import db
from app.modules.common.model import Model


class Comment(Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
