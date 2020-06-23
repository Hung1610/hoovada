from app import db
from app.modules.common.model import Model


class Follow(Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    followed_id = db.Column(db.Integer)
