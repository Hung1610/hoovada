#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from app.app import db
from common.enum import ReportTypeEnum
from common.models.model import Model

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


class AnswerReport(Model, BaseReport):
    __tablename__ = 'answer_report'

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer


class AnswerCommentReport(Model, BaseReport):
    __tablename__ = 'answer_comment_report'

    comment_id = db.Column(db.Integer, db.ForeignKey('answer_comment.id'), nullable=False)
    comment = db.relationship('AnswerComment', lazy=True) # one-to-many relationship with table Comment


class ArticleReport(Model, BaseReport):
    __tablename__ = 'article_report'
    
    article_id = db.Column(db.Integer)


class ArticleCommentReport(Model, BaseReport):
    __tablename__ = 'article_comment_report'
    comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'), nullable=False)
    comment = db.relationship('ArticleComment', lazy=True) # one-to-many relationship with table Comment


class PostReport(Model, BaseReport):
    __tablename__ = 'post_report'
    
    post_id = db.Column(db.Integer)


class TopicReport(Model, BaseReport):
    __tablename__ = 'topic_report'
    
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic
