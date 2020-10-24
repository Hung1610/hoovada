from app import db
from app.common.model import Model


class ArticleShare(Model):
    __tablename__ = 'article_share'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shared_by_user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    shared_article = db.relationship('Article', lazy=True) # one-to-many relationship with table Article
    created_date = db.Column(db.Date)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)
