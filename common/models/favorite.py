#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from common.models.model import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

# pylint: disable=no-self-use
class BaseFavorite(object):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionFavorite(Model, BaseFavorite):
    __tablename__ = 'question_favorite'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question


class AnswerFavorite(Model, BaseFavorite):
    __tablename__ = 'answer_favorite'

    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer


class AnswerCommentFavorite(Model, BaseFavorite):
    __tablename__ = 'answer_comment_favorite'
    
    answer_comment_id = db.Column(db.Integer, db.ForeignKey('answer_comment.id'), nullable=False)
    answer_comment = db.relationship('AnswerComment', lazy=True) # one-to-many relationship with table AnswerComment


class ArticleFavorite(Model, BaseFavorite):
    __tablename__ = 'article_favorite'
    
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', lazy=True) # one-to-many relationship with table Article


class ArticleCommentFavorite(Model, BaseFavorite):
    __tablename__ = 'article_comment_favorite'

    article_comment_id = db.Column(db.Integer, db.ForeignKey('article_comment.id'), nullable=False)
    article_comment = db.relationship('ArticleComment', lazy=True) # one-to-many relationship with table QuestionComment


class PostFavorite(Model, BaseFavorite):
    __tablename__ = 'post_favorite'
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', lazy=True) # one-to-many relationship with table Post
