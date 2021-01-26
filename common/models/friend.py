#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g

# own modules
from common.db import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFriend(Model):
    __tablename__ = 'user_friend'

    id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), index=True)
    friend = db.relationship('User', foreign_keys=[friend_id], backref='sent_friend_requests', lazy=True) # one-to-many relationship with table User
    friended_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    friended = db.relationship('User', foreign_keys=[friended_id], backref='received_friend_requests', lazy=True) # one-to-many relationship with table User
    is_approved = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)

    @property
    def adaptive_friend(self):
        if g.friend_belong_to_user_id or len(g.mutual_friend_ids) > 0:
            return self.friend if self.friended_id == g.friend_belong_to_user_id \
                or (self.friended_id in g.mutual_friend_ids)\
                else self.friended

        return None

    @property
    def adaptive_friend_id(self):
        if g.friend_belong_to_user_id or len(g.mutual_friend_ids) > 0:
            return self.friend_id if self.friended_id == g.friend_belong_to_user_id \
                or (self.friended_id in g.mutual_friend_ids)\
                else self.friended_id

        return None

    @property
    def adaptive_friended(self):
        if g.friend_belong_to_user_id or len(g.mutual_friend_ids) > 0:
            return self.friended if self.friended_id != self.adaptive_friend_id\
                else self.friend

        return self.friend

    @property
    def adaptive_friended_id(self):
        if g.friend_belong_to_user_id or len(g.mutual_friend_ids) > 0:
            return self.friended_id if self.friended_id != self.adaptive_friend_id\
                else self.friend_id

        return None
