from app import db
from app.common.model import Model


class UserPermission(Model):
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), index=True)
    permission_id = db.Column(db.ForeignKey('permission.id'), index=True)
    allow = db.Column(db.Boolean, default=False)
