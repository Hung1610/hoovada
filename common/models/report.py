#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from common.db import db
from common.enum import ReportTypeEnum, EntityTypeEnum
from common.models.model import Model
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseReport(OrganizationRole):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    report_type = db.Column(db.Enum(ReportTypeEnum, validate_strings=True), nullable=False, server_default="GENERAL")
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionReport(Model, BaseReport):
    __tablename__ = 'question_report'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False, index=True)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question
    duplicated_question_id = db.Column(db.Integer, nullable=True, index=True)


class QuestionCommentReport(Model, BaseReport):
    __tablename__ = 'question_comment_report'

    comment_id = db.Column(db.Integer, db.ForeignKey('question_comment.id', ondelete='CASCADE'), nullable=False, index=True)
    comment = db.relationship('QuestionComment', lazy=True) # one-to-many relationship with table Comment


class AnswerReport(Model, BaseReport):
    __tablename__ = 'answer_report'

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=False, index=True)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer


class AnswerCommentReport(Model, BaseReport):
    __tablename__ = 'answer_comment_report'

    comment_id = db.Column(db.Integer, db.ForeignKey('answer_comment.id', ondelete='CASCADE'), nullable=False, index=True)
    comment = db.relationship('AnswerComment', lazy=True) # one-to-many relationship with table Comment


class ArticleReport(Model, BaseReport):
    __tablename__ = 'article_report'
    
    article_id = db.Column(db.Integer, index=True)


class ArticleCommentReport(Model, BaseReport):
    __tablename__ = 'article_comment_report'
    comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id', ondelete='CASCADE'), nullable=False, index=True)
    comment = db.relationship('ArticleComment', lazy=True) # one-to-many relationship with table Comment


class PostReport(Model, BaseReport):
    __tablename__ = 'post_report'
    post_id = db.Column(db.Integer, index=True)

class PostCommentReport(Model, BaseReport):
    __tablename__ = 'post_comment_report'

    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id', ondelete='CASCADE'), nullable=False, index=True)
    comment = db.relationship('PostComment', lazy=True) # one-to-many relationship with table Comment


class TopicReport(Model, BaseReport):
    __tablename__ = 'topic_report'
    
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic


class PollReport(Model, BaseReport):
    __tablename__ = 'poll_report'
    poll_id = db.Column(db.Integer, index=True)

class PollCommentReport(Model, BaseReport):
    __tablename__ = 'poll_comment_report'

    comment_id = db.Column(db.Integer, db.ForeignKey('poll_comment.id', ondelete='CASCADE'), nullable=False, index=True)
    comment = db.relationship('PollComment', lazy=True) # one-to-many relationship with table Comment
