#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from sqlalchemy.ext.declarative import declared_attr

# own modules
from app import db
from common.models.model import Model
from common.enum import ReportTypeEnum

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseReport(object):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    report_type = db.Column(db.Enum(ReportTypeEnum, validate_strings=True), nullable=False, server_default="GENERAL")
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionReport(Model, BaseReport):
    __tablename__ = 'question_report'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question


class ArticleReport(Model, BaseReport):
    __tablename__ = 'article_report'
    
    article_id = db.Column(db.Integer)


class PostReport(Model, BaseReport):
    __tablename__ = 'post_report'
    
    post_id = db.Column(db.Integer)
