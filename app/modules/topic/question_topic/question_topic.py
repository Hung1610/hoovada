from datetime import datetime

from app import db
from app.modules.common.model import Model


class QuestionTopic(Model):
    __tablename__ = 'question_topic'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
