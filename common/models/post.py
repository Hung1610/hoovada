#!/usr/bin/env python
# -*- coding: utf-8 -*-


# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from common.models.mixins import AnonymousMixin, AuditCreateMixin, AuditUpdateMixin, SoftDeleteMixin
from common.db import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

post_topics = db.Table('topic_post',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), primary_key=True),
    extend_existing=True
)

class Post(Model, SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Post
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=True, index=True)
    fixed_topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Post
    html = db.Column(db.UnicodeText)
    file_url = db.Column(db.String(255))
    views_count = db.Column(db.Integer, default=0)

    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status == 'UPVOTED'"), 1, 0)))
    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status == 'DOWNVOTED'"), 1, 0)))
    @aggregated('post_shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')
    @aggregated('post_comments', db.Column(db.Integer))
    def comment_count(self):
        return db.func.count('1')

    topics = db.relationship('Topic', secondary=post_topics, lazy='subquery')
    scheduled_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    allow_favorite = db.Column(db.Boolean, default=True, server_default=expression.true())
    is_draft = db.Column(db.Boolean, server_default=expression.false())
    votes = db.relationship("PostVote", cascade='all,delete-orphan')
    post_comments = db.relationship("PostComment", cascade='all,delete-orphan',
                    primaryjoin="and_(Post.id == remote(PostComment.post_id),\
                        remote(PostComment.user_id) == User.id, remote(User.is_deactivated) == False)")
    post_shares = db.relationship("PostShare", cascade='all,delete-orphan')
    