#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from common.models.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFriend(Model):
    __tablename__ = 'user_friend'

    id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    friend = db.relationship('User', foreign_keys=[friend_id], backref='friends', lazy=True) # one-to-many relationship with table User
    friended_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friended = db.relationship('User', foreign_keys=[friended_id], backref='friend_requests', lazy=True) # one-to-many relationship with table User
    is_approved = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
