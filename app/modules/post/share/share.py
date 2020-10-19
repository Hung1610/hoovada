from app import db
from app.modules.common.model import Model


class PostShare(Model):
    __tablename__ = 'post_share'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shared_by_user = db.relationship('User', lazy=True) # one-to-many relationship with table Post
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    shared_post = db.relationship('Post', lazy=True) # one-to-many relationship with table Post
    created_date = db.Column(db.Date)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)
