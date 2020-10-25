#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from app import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class AnswerReport(Model):
    __tablename__ = 'answer_report'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer
    inappropriate = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime)
