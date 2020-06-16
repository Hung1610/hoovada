from datetime import datetime
from app import db
from app.modules.common.model import Model


class Answer(Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    upvote_count = db.Column(db.Integer, default=0)
    downvote_count = db.Column(db.Integer, default=0)
    anonymous = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean, default=False)
    answer = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    image_ids = db.Column(db.JSON)
    user_hidden = db.Column(db.Boolean, default=False)
