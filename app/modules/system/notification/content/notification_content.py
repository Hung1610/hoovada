from app import db
from common.models.model import Model


class NotificationContent(Model):
    __tablename__ = 'notification_content'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    created_date = db.Column(db.DateTime)
