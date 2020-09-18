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


class AnswerShare(Model):
    __tablename__ = 'answer_share'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='answer_shares', lazy=True) # one-to-many relationship with table Article
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Article
    created_date = db.Column(db.Date)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)

