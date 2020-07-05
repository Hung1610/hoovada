from app import db
from app.modules.common.model import Model


class Report(Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    inappropriate = db.Column(db.Boolean)
    description = db.Column(db.String)
    created_date = db.Column(db.DateTime)
