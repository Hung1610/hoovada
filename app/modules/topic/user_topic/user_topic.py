from app.modules.common.model import Model

from app.app import db


class UserTopic(Model):
    __tablename__ = 'user_topic'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)
