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
from app.modules.common.model import Model
from app.modules.post.voting.vote import PostVote

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

post_topics = db.Table('topic_post',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    extend_existing=True
)

class Post(Model):
    __tablename__ = 'post'
    __table_args__ = (
        db.Index("idx_post_title", "title", mysql_length=255),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    slug = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Post
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)
    fixed_topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Post
    html = db.Column(db.UnicodeText)
    file_url = db.Column(db.String(255))
    views_count = db.Column(db.Integer, default=0)

    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.sum(db.func.if_(PostVote.vote_status == 'UPVOTED', 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.sum(db.func.if_(PostVote.vote_status == 'DOWNVOTED', 1, 0))
    @aggregated('post_shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')
    @aggregated('post_favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')
    @aggregated('post_comments', db.Column(db.Integer))
    def comment_count(self):
        return db.func.count('1')

    topics = db.relationship('Topic', secondary=post_topics, lazy='subquery')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_draft = db.Column(db.Boolean, server_default=expression.false())
    is_deleted = db.Column(db.Boolean, default=False, server_default=expression.false())
    votes = db.relationship("PostVote", cascade='all,delete-orphan')
    post_favorites = db.relationship("PostFavorite", cascade='all,delete-orphan')
    post_comments = db.relationship("PostComment", cascade='all,delete-orphan')
    post_shares = db.relationship("PostShare", cascade='all,delete-orphan')

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

event.listen(Post.title, 'set', Post.generate_slug, retval=False)