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

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class BaseComment(object):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText)
    allow_favorite = db.Column(db.Boolean, default=True)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_creator_deactivated(self):
        if self.user:
            return True if self.user.is_deactivated else False
        return False
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class ArticleComment(Model, BaseComment):
    __tablename__ = 'article_comment'

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index=True)
    article = db.relationship('Article', lazy=True)
    favorites = db.relationship("ArticleCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')


class PostComment(Model, BaseComment):
    __tablename__ = 'post_comment'
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)
    post = db.relationship('Post', lazy=True) 
    

class AnswerComment(Model, BaseComment):
    __tablename__ = 'answer_comment'
    
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), index=True)
    answer = db.relationship('Answer', lazy=True)
    favorites = db.relationship("AnswerCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')


class QuestionComment(Model, BaseComment):
    __tablename__ = 'question_comment'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), index=True)
    question = db.relationship('Question', lazy=True)
    favorites = db.relationship("QuestionCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')

