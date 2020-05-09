from app import db
from app.modules.common.model import Model


class Reputation(Model):
    __tablename__ = 'reputation'

    reputation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)
    score = db.Column(db.Float)
    created_date = db.Column(db.DateTime)
