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
from common.models.model import Model
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

# pylint: disable=R0201
class BaseBookmark(OrganizationRole):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionBookmark(Model, BaseBookmark):
    __tablename__ = 'question_bookmark'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question


class AnswerBookmark(Model, BaseBookmark):
    __tablename__ = 'answer_bookmark'

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=False)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer


class TopicBookmark(Model, BaseBookmark):
    __tablename__ = 'topic_bookmark'
    
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic


class ArticleBookmark(Model, BaseBookmark):
    __tablename__ = 'article_bookmark'

    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), nullable=False)
    article = db.relationship('Article', lazy=True)  # one-to-many relationship with table Article

class PollBookmark(Model, BaseBookmark):
    __tablename__ = 'poll_bookmark'

    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id', ondelete='CASCADE'), nullable=False)
    poll = db.relationship('Poll', lazy=True)  # one-to-many relationship with table Article
