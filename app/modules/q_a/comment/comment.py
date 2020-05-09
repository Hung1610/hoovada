from app import db
from app.modules.common.model import Model


class Comment(Model):
    __tablename__ = 'comment'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
