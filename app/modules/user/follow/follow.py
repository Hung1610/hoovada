#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from app.common.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFollow(Model):
    __tablename__ = 'user_follow'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    follower = db.relationship('User', foreign_keys=[follower_id], lazy=True) # one-to-many relationship with table User
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed = db.relationship('User', foreign_keys=[followed_id], lazy=True) # one-to-many relationship with table User
    is_approved = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
