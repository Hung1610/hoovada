#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

article_topics = db.Table('topic_article',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
)

class Article(Model):
    __tablename__ = 'article'
    __table_args__ = (
        db.Index("idx_article_title", "title", mysql_length=255),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    article_by_user = db.relationship('User', backref='articles', lazy=True) # one-to-many relationship with table Article
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'),
        nullable=False)
    fixed_topic = db.relationship('Topic', backref='fixed_topic_articles', lazy=True) # one-to-many relationship with table Article
    html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    upvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly upvote
    downvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly downvote
    share_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    topics = db.relationship('Topic', secondary=article_topics, lazy='subquery',
        backref=db.backref('articles', lazy=True))
