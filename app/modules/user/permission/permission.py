from app import db
from app.modules.common.model import Model


class Permission(Model):
    __tablename__ = 'permission'

    permission_id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String, required=True)
    description = db.Column(db.String)
