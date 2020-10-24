#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from slugify import slugify
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from sqlalchemy import event

# own modules
from app import db
from app.common.model import Model
from app.modules.article.voting.vote import ArticleVote

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

article_topics = db.Table('topic_article',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    extend_existing=True
)

class Article(Model):
    __tablename__ = 'article'
    __table_args__ = (
        db.Index("idx_article_title", "title", mysql_length=255),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    slug = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_by_user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    fixed_topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Article
    html = db.Column(db.UnicodeText)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    views_count = db.Column(db.Integer, default=0)

    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.sum(db.func.if_(ArticleVote.vote_status == 'UPVOTED', 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.sum(db.func.if_(ArticleVote.vote_status == 'DOWNVOTED', 1, 0))
    @aggregated('article_shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')
    @aggregated('article_favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')
    @aggregated('article_comments', db.Column(db.Integer))
    def comment_count(self):
        return db.func.count('1')

    topics = db.relationship('Topic', secondary=article_topics, lazy='subquery')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_draft = db.Column(db.Boolean, server_default=expression.false())
    is_deleted = db.Column(db.Boolean, default=False, server_default=expression.false())
    votes = db.relationship("ArticleVote", cascade='all,delete-orphan')
    article_favorites = db.relationship("ArticleFavorite", cascade='all,delete-orphan')
    article_comments = db.relationship("ArticleComment", cascade='all,delete-orphan')
    article_shares = db.relationship("ArticleShare", cascade='all,delete-orphan')

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

event.listen(Article.title, 'set', Article.generate_slug, retval=False)