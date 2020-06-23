from app import db
from app.modules.common.model import Model


class Message(Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.UnicodeText)
    sent_time = db.Column(db.DateTime)
    read_time = db.Column(db.DateTime)
    sender_id = db.Column(db.Integer)
    recipient_id = db.Column(db.Integer)
