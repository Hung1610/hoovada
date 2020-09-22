#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AnswerComment(Model):
    __tablename__ = 'answer_comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer =  db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.relationship("AnswerCommentVote", cascade='all,delete-orphan')
    favorites = db.relationship("AnswerCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')

