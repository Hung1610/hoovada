#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app import db
from common.models.model import Model


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionShare(Model):
    __tablename__ = 'question_share'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], lazy=True) # one-to-many relationship with table Article
    user_shared_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_shared_to = db.relationship('User', foreign_keys=[user_shared_to_id], lazy=True) # one-to-many relationship with table Article
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Article
    created_date = db.Column(db.Date)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)

