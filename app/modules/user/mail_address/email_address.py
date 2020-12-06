from common.db import db
from common.models.model import Model


class EmailAddress(Model):
    __tablename__ = 'email_address'

    id = db.Column(db.Integer)
    email = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    updated_date = db.Column(db.DateTime)
