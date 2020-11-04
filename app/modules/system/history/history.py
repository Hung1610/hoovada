from app.app import db
from common.models.model import Model


class History(Model):
    __tablename__ = 'history'

    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    log = db.Column(db.String(500))
    created_date = db.Column(db.Date)
    created_time = db.Column(db.Time)
    critical_score = db.Column(db.Integer)
