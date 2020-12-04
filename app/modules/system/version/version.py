from common.models.model import db
from common.models.model import Model


class Version(Model):
    __tablename__ = 'alembic_version'

    # alembic_version_id = db.Column(db.Integer, primary_key=True)
    version_num = db.Column(db.String)
