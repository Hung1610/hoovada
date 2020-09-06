#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from app.modules.common.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicBookmark(Model):
    __tablename__ = 'topic_bookmark'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref='topic_bookmarks', lazy=True) # one-to-many relationship with table User
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', backref='topic_bookmarks', lazy=True) # one-to-many relationship with table Topic
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
