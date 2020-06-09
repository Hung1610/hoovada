from app import db
from app.modules.common.model import Model


class Vote(Model):
    __tablename__ = 'voting'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    up_vote = db.Column(db.Boolean)
    down_vote = db.Column(db.Boolean)
    voting_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
