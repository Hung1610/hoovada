#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from common.models.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class PostFavorite(Model):
    __tablename__ = 'post_favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', lazy=True) # one-to-many relationship with table Post
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
