from app import db
from app.modules.common.model import Model


class NotificationContent(Model):
    __tablename__ = 'notification_content'

    content_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    created_date = db.Column(db.Date)
    created_time = db.Column(db.Time)
