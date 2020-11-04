#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app.app import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicReport(Model):
    __tablename__ = 'topic_report'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic
    inappropriate = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime)
