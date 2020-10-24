from app import db
from app.common.model import Model


class Feedback(Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True)
    overall_rate = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    created_date = db.Column(db.Date)
    created_time = db.Column(db.Time)
    user_id = db.Column(db.Integer)
    question_quality = db.Column(db.Integer)
    answer_quality = db.Column(db.Integer)
    bandwidth_quality = db.Column(db.Integer)
    support_quality = db.Column(db.Integer)
