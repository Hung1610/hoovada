#!/usr/bin/env python
# -*- coding: utf-8 -*-


# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from sqlalchemy.sql import expression
from sqlalchemy.sql import func
from sqlalchemy_utils import aggregated
from flask import g

# own modules
from common.models.mixins import AnonymousMixin, AuditCreateMixin, AuditUpdateMixin
from common.db import db
from common.models.model import Model
from common.enum import EntityTypeEnum
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Post(Model, AuditCreateMixin, AuditUpdateMixin, AnonymousMixin, OrganizationRole):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', lazy=True)
    html = db.Column(db.UnicodeText)
    file_url = db.Column(db.String(255))
    views_count = db.Column(db.Integer, server_default="0", nullable=False)

    @aggregated('post_shares', db.Column(db.Integer, server_default="0", nullable=False))
    def share_count(self):
        return db.func.count('1')
    
    @aggregated('post_favorites', db.Column(db.Integer, server_default="0", nullable=False))
    def favorite_count(self):
        return db.func.count('1')

    @aggregated('post_comments', db.Column(db.Integer, server_default="0", nullable=False))
    def comment_count(self):
        return db.func.count('1')

    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, server_default=func.now())
    allow_favorite = db.Column(db.Boolean, server_default=expression.true())
    allow_comments = db.Column(db.Boolean, server_default=expression.true())

    post_comments = db.relationship("PostComment", cascade='all,delete-orphan', primaryjoin="and_(Post.id == remote(PostComment.post_id), remote(PostComment.user_id) == User.id, remote(User.is_deactivated) == False)")
    post_shares = db.relationship("PostShare", cascade='all,delete-orphan')
    post_favorites = db.relationship("PostFavorite", cascade='all,delete-orphan')

    @property
    def is_favorited_by_me(self):
        PostFavorite = db.get_model('PostFavorite')
        if g.current_user:
            favorite = PostFavorite.query.filter(PostFavorite.user_id == g.current_user.id, PostFavorite.post_id == self.id).first()
            return True if favorite is not None else False
            
        return False
