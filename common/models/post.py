#!/usr/bin/env python
# -*- coding: utf-8 -*-


# built-in modules
from datetime import datetime

# third-party modules
from flask import g
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


class Post(Model, SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', lazy=True)
    html = db.Column(db.UnicodeText)
    file_url = db.Column(db.String(255))
    views_count = db.Column(db.Integer, server_default=0)

    @aggregated('post_shares', db.Column(db.Integer, server_default="0", nullable=False))
    def share_count(self):
        return db.func.count('1')
    
    @aggregated('post_favorites', db.Column(db.Integer, server_default="0", nullable=False))
    def favorite_count(self):
        return db.func.count('1')

    @aggregated('post_comments', db.Column(db.Integer, server_default="0", nullable=False))
    def comment_count(self):
        return db.func.count('1')

    scheduled_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, server_default=datetime.utcnow)
    allow_favorite = db.Column(db.Boolean, server_default=expression.true())
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    is_draft = db.Column(db.Boolean, server_default=expression.false())
    post_comments = db.relationship("PostComment", cascade='all,delete-orphan', primaryjoin="and_(Post.id == remote(PostComment.post_id), remote(PostComment.user_id) == User.id, remote(User.is_deactivated) == False)")
    post_shares = db.relationship("PostShare", cascade='all,delete-orphan')
    post_favorites = db.relationship("PostFavorite", cascade='all,delete-orphan')

    @property
    def is_seen_by_me(self):
        UserSeenPost = db.get_model('UserSeenPost')
        if g.current_user:
            seen = UserSeenPost.query.with_entities(UserSeenPost.id).filter(UserSeenPost.user_id == g.current_user.id,
                                                                          UserSeenPost.post_id == self.id).first()
            return True if seen else False
        return False