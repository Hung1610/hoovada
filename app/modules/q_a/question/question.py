from app import db
from app.modules.common.model import Model


class Question(Model):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer)
    _question = db.Column(db.UnicodeText)
    _markdown = db.Column(db.UnicodeText)
    _html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    views = db.Column(db.Integer)
    last_activity = db.Column(db.DateTime)
    answers_allowed = db.Column(db.Integer)
    accepted_answer_id = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean)
    image_ids = db.Column(db.JSON)
