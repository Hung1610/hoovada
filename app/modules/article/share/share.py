from app import db
from app.modules.common.model import Model


class Share(Model):
    __tablename__ = 'share'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    answer_id = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    anonymous = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)
