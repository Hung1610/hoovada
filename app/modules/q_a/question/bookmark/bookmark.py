#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from app.modules.common.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionBookmark(Model):
    __tablename__ = 'question_bookmark'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref='question_bookmarks', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', cascade='all, delete', backref='question_bookmarks', lazy=True) # one-to-many relationship with table Question
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
