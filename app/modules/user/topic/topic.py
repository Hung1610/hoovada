#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserTopic(Model):
    __tablename__ = 'user_topic'

    id = db.Column(db.Integer, primary_key=True)
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    fixed_topic = db.relationship('Topic', foreign_keys=[fixed_topic_id], backref='fixed_topic_user_experiences', lazy=True) # one-to-many relationship with table Article
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', foreign_keys=[topic_id], backref='topic_user_experiences', lazy=True) # one-to-many relationship with table Article
    description = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', backref='user_topics_experiences', lazy=True) # one-to-many relationship with table Article
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

