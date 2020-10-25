#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from common.models.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AnswerBookmark(Model):
    __tablename__ = 'answer_bookmark'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
