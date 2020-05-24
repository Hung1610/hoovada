from app import db
from app.modules.common.model import Model


class UserPermission(Model):
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    permission_id = db.Column(db.Integer)
