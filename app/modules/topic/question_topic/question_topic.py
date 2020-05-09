from app import db
from app.modules.common.model import Model


class QuestionTopic(Model):
    __tablename__ = 'question_topic'

    question_topic_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)
