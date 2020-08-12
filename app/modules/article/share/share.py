from app import db
from app.modules.common.model import Model


class Share(Model):
    __tablename__ = 'article_share'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    shared_by_user = db.relationship('User', backref='shares', lazy=True) # one-to-many relationship with table Article
    article_id = db.Column(db.Integer)
    shared_article = db.relationship('Article', backref='shares', lazy=True) # one-to-many relationship with table Article
    created_date = db.Column(db.Date)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    anonymous = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)
