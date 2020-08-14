#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy_utils import aggregated

# own modules
from app import db
from app.modules.common.model import Model
from app.modules.article.voting.vote import ArticleVote

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
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    views_count = db.Column(db.Integer, default=0)
    # TODO: convert these to custom property 
    # upvote_count = db.Column(db.Integer, default=0) 
    # downvote_count = db.Column(db.Integer, default=0)  
    # share_count = db.Column(db.Integer, default=0)
    # favorite_count = db.Column(db.Integer, default=0)

    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.sum(db.func.if_(ArticleVote.vote_status == 'UPVOTED', 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.sum(db.func.if_(ArticleVote.vote_status == 'DOWNVOTED', 1, 0))
    @aggregated('shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')
    @aggregated('article_favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')
    #
    topics = db.relationship('Topic', secondary=article_topics, lazy='subquery',
        backref=db.backref('articles', lazy=True))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
