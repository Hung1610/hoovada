#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

# built-in modules
from slugify import slugify

# third-party modules
from sqlalchemy import event
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from common.db import db
from common.models.mixins import AnonymousMixin, AuditCreateMixin, AuditUpdateMixin, SoftDeleteMixin
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

article_topics = db.Table('topic_article',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

class Article(Model, SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin, AnonymousMixin):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    slug = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)
    fixed_topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Article
    html = db.Column(db.UnicodeText)
    allow_voting = db.Column(db.Boolean, default=True)
    views_count = db.Column(db.Integer, default=0)

    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def upvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'UPVOTED'"), 1, 0)), 0)
    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def downvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'DOWNVOTED'"), 1, 0)), 0)
    @aggregated('article_shares', db.Column(db.Integer, server_default="0", nullable=False))
    def share_count(self):
        return db.func.count('1')
    @aggregated('article_favorites', db.Column(db.Integer, server_default="0", nullable=False))
    def favorite_count(self):
        return db.func.count('1')
    @aggregated('article_comments', db.Column(db.Integer, server_default="0", nullable=False))
    def comment_count(self):
        return db.func.count('1')

    topics = db.relationship('Topic', secondary=article_topics, backref='articles', lazy='subquery')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_draft = db.Column(db.Boolean, server_default=expression.false())
    votes = db.relationship("ArticleVote", cascade='all,delete-orphan')
    article_favorites = db.relationship("ArticleFavorite", cascade='all,delete-orphan')
    article_comments = db.relationship("ArticleComment", cascade='all,delete-orphan',
                    primaryjoin="and_(Article.id == remote(ArticleComment.article_id),\
                        remote(ArticleComment.user_id) == User.id, remote(User.is_deactivated) == False)")
    article_shares = db.relationship("ArticleShare", cascade='all,delete-orphan')

    @property
    def is_bookmarked_by_me(self):
        ArticleBookmark = db.get_model('ArticleBookmark')
        if g.current_user:
            bookmark = ArticleBookmark.query.filter(ArticleBookmark.user_id == g.current_user.id,
                                                    ArticleBookmark.article_id == self.id).first()
            return True if bookmark else False
        return False

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

event.listen(Article.title, 'set', Article.generate_slug, retval=False)
