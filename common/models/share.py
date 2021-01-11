#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from common.db import db
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseShare(object):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    facebook = db.Column(db.Boolean)
    twitter = db.Column(db.Boolean)
    linkedin = db.Column(db.Boolean)
    zalo = db.Column(db.Boolean)
    vkontakte = db.Column(db.Boolean)
    mail = db.Column(db.Boolean)
    link_copied = db.Column(db.Boolean)
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionShare(Model, BaseShare):
    __tablename__ = 'question_share'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    user = db.relationship('User', foreign_keys=[user_id], lazy=True)
    user_shared_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user_shared_to = db.relationship('User', foreign_keys=[user_shared_to_id], lazy=True) # one-to-many relationship with table Article
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), index=True)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Article


class AnswerShare(Model, BaseShare):
    __tablename__ = 'answer_share'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), index=True)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Article


class ArticleShare(Model, BaseShare):
    __tablename__ = 'article_share'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index=True)
    article = db.relationship('Article', lazy=True) # one-to-many relationship with table Article


class PostShare(Model, BaseShare):
    __tablename__ = 'post_share'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Post
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)
    post = db.relationship('Post', lazy=True) # one-to-many relationship with table Post


class TopicShare(Model, BaseShare):
    __tablename__ = 'topic_share'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), index=True)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Article