#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app.app import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionCommentFavorite(Model):
    __tablename__ = 'question_comment_favorite'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    question_comment_id = db.Column(db.Integer, db.ForeignKey('question_comment.id'), nullable=False)
    question_comment = db.relationship('QuestionComment', lazy=True) # one-to-many relationship with table QuestionComment
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)

