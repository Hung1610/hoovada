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


class ArticleFavorite(Model, BaseFavorite):
    __tablename__ = 'article_favorite'
    
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    article = db.relationship('Article', lazy=True) # one-to-many relationship with table Article


class PostFavorite(Model, BaseFavorite):
    __tablename__ = 'post_favorite'
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', lazy=True) # one-to-many relationship with table Post
