from app import db
from app.modules.common.model import Model


class Follow(Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    followed_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
