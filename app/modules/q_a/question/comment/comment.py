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


class QuestionComment(Model):
    __tablename__ = 'question_comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.relationship("QuestionCommentVote", cascade='all,delete-orphan')

