#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from common.db import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseFollow(object):
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserFollow(Model, BaseFollow):
    __tablename__ = 'user_follow'
    
    follower_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    follower = db.relationship('User', foreign_keys=[follower_id], lazy=True) # one-to-many relationship with table User
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed = db.relationship('User', foreign_keys=[followed_id], lazy=True) # one-to-many relationship with table User


class TopicFollow(Model, BaseFollow):
    __tablename__ = 'topic_follow'
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic