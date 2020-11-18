#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app.app import db
from common.enum import TimelineActivityEnum
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Timeline(Model):
    __tablename__ = 'timeline'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question_comment_id = db.Column(db.Integer, db.ForeignKey('question_comment.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer_comment_id = db.Column(db.Integer, db.ForeignKey('answer_comment.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article_comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'))
    activity = db.Column(db.Enum(TimelineActivityEnum, validate_strings=True))
    activity_date = db.Column(db.DateTime, default=datetime.utcnow)
