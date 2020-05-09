from app import db
from app.modules.common.model import Model


class Notification(Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String)
    content_id = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    created_time = db.Column(db.Time)
    seen_date = db.Column(db.Date)
    seen_time = db.Column(db.Time)
    viewed = db.Column(db.Boolean)
    emailed = db.Column(db.Boolean)
