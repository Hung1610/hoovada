#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from common.db import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class QuestionCommentReport(Model):
    __tablename__ = 'question_comment_report'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    comment_id = db.Column(db.Integer, db.ForeignKey('question_comment.id'), nullable=False)
    comment = db.relationship('QuestionComment', lazy=True) # one-to-many relationship with table Comment
    inappropriate = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime)
