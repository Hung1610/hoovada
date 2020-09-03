#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum
from datetime import datetime

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TimelineActivity(enum.Enum):
    COMMENTED = 1
    FAVORITED = 2
    UPVOTED = 3
    DOWNVOTED = 4
    REPORTED = 5


class Timeline(Model):
    __tablename__ = 'timeline'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='timelines', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article_comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'))
    activity = db.Column(db.Enum(TimelineActivity, validate_strings=True))
    activity_date = db.Column(db.DateTime, default=datetime.utcnow)
