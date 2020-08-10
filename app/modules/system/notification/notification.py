from app import db
from app.modules.common.model import Model


class Notification(Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(255))
    content_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime)
    seen_date = db.Column(db.DateTime)
    viewed = db.Column(db.Boolean)
    emailed = db.Column(db.Boolean)
