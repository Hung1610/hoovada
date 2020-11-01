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
from common.enum import VotingStatusEnum

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseVote(object):
    id = db.Column(db.Integer, primary_key=True)
    vote_status = db.Column(db.Enum(VotingStatusEnum, validate_strings=True), nullable=False, server_default="NEUTRAL")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionVote(Model, BaseVote):
    __tablename__ = 'question_vote'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question


class ArticleVote(Model, BaseVote):
    __tablename__ = 'article_vote'

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Article', lazy=True) # one-to-many relationship with table Article


class ArticleCommentVote(Model, BaseVote):
    __tablename__ = 'article_comment_vote'
    
    comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'))
    comment = db.relationship('ArticleComment', lazy=True) # one-to-many relationship with table Comment


class PostVote(Model, BaseVote):
    __tablename__ = 'post_vote'
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', lazy=True) # one-to-many relationship with table Post