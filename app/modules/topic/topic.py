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


class Topic(Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    count = db.Column(db.Integer, default=0) # chua ro truong nay su dung lam gi
    user_id = db.Column(db.Integer)  # who created this topic
    question_count = db.Column(db.Integer, default=0)  # amount of question related to this topic
    user_count = db.Column(db.Integer, default=0)  # Number of users who interest this topic
    answer_count = db.Column(db.Integer, default=0)  # how many answers related to this topic
    parent_id = db.Column(db.Integer)  # the ID of parent topic
    is_fixed = db.Column(db.Boolean, default=False)  # is this topic fixed?
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))

    fixed_topic_articles = db.relationship('Article', backref='fixed_topic', lazy=True) # one-to-many relationship with table Article
