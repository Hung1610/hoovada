from app import db
from app.modules.common.model import Model


class Permission(Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(255), required=True)
    description = db.Column(db.String(255))
