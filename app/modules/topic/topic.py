from app import db
from app.modules.common.model import Model


class Topic(Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer)  # who created this topic
    question_count = db.Column(db.Integer)  # amount of question related to this topic
    user_count = db.Column(db.Integer)  # Number of users who interest this topic
    answer_count = db.Column(db.Integer)  # how many answers related to this topic
    parent_id = db.Column(db.Integer) # the ID of parent topic
    is_fixed = db.Column(db.Boolean)    # is this topic fixed?
