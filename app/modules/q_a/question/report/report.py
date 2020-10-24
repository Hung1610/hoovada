#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum

# own modules
from app import db
from app.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReportTypeEnum(enum.Enum):
    GENERAL = 1
    INAPPROPRIATE = 2
    DUPLICATE = 3


class QuestionReport(Model):
    __tablename__ = 'question_report'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question
    report_type = db.Column(db.Enum(ReportTypeEnum, validate_strings=True), nullable=False, server_default="GENERAL")
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime)
