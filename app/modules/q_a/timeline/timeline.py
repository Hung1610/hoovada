from app import db
from app.modules.common.model import Model


class TimeLine(Model):
    __tablename__ = 'timeline'

    timeline_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    activity = db.Column(db.String)
    activity_date = db.Column(db.Date)
    activity_time = db.Column(db.Time)
