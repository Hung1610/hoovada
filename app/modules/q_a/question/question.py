from datetime import datetime

from app import db
from app.modules.common.model import Model


class Question(Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer)
    fixed_topic_id = db.Column(db.Integer)
    fixed_topic_name = db.Column(db.String)
    question = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    answers_count = db.Column(db.Integer, default=0)
    accepted_answer_id = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean, default=False)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    upvote_count = db.Column(db.Integer, default=0)
    downvote_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
