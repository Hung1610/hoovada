from app import db
from app.modules.common.model import Model


class Favorite(Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    favorited_user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    updated_time = db.Column(db.Time)
