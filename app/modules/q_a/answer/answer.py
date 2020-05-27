from app import db
from app.modules.common.model import Model


class Answer(Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime)
    upvote_count = db.Column(db.Integer)
    downvote_count = db.Column(db.Integer)
    anonymous = db.Column(db.Integer)
    accepted = db.Column(db.Boolean)
    answer_body = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    image_ids = db.Column(db.JSON)
