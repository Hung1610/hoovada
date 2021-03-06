#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from flask import g

# own modules
from common.db import db
from common.models.model import Model
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class BaseComment(OrganizationRole):
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
        return db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class ArticleComment(Model, BaseComment):
    __tablename__ = 'article_comment'

    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), index=True)
    article = db.relationship('Article', lazy=True)
    favorites = db.relationship("ArticleCommentFavorite", cascade='all,delete-orphan')

    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')

    @property
    def is_favorited_by_me(self):
        ArticleCommentFavorite = db.get_model('ArticleCommentFavorite')
        if g.current_user:
            favorite = ArticleCommentFavorite.query.filter(ArticleCommentFavorite.user_id == g.current_user.id, ArticleCommentFavorite.article_comment_id == self.id).first()
            if favorite is not None:
                return True
        return False


class PostComment(Model, BaseComment):
    __tablename__ = 'post_comment'
    
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), index=True)
    post = db.relationship('Post', lazy=True) 
    favorites = db.relationship("PostCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')  

    @property
    def is_favorited_by_me(self):
        PostCommentFavorite = db.get_model('PostCommentFavorite')
        if g.current_user:
            favorite = PostCommentFavorite.query.filter(PostCommentFavorite.user_id == g.current_user.id, PostCommentFavorite.post_comment_id == self.id).first()
            if favorite is not None:
                return True
        return False


class AnswerComment(Model, BaseComment):
    __tablename__ = 'answer_comment'
    
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), index=True)
    answer = db.relationship('Answer', lazy=True)
    favorites = db.relationship("AnswerCommentFavorite", cascade='all,delete-orphan')

    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')

    @property
    def is_favorited_by_me(self):
        AnswerCommentFavorite = db.get_model('AnswerCommentFavorite')
        if g.current_user:
            favorite = AnswerCommentFavorite.query.filter(AnswerCommentFavorite.user_id == g.current_user.id, AnswerCommentFavorite.answer_comment_id == self.id).first()
            if favorite is not None:
                return True
        return False


class QuestionComment(Model, BaseComment):
    __tablename__ = 'question_comment'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), index=True)
    question = db.relationship('Question', lazy=True)
    favorites = db.relationship("QuestionCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')

    @property
    def is_favorited_by_me(self):
        QuestionCommentFavorite = db.get_model('QuestionCommentFavorite')
        if g.current_user:
            favorite = QuestionCommentFavorite.query.filter(QuestionCommentFavorite.user_id == g.current_user.id, QuestionCommentFavorite.question_comment_id == self.id).first()
            if favorite is not None:
                return True
        return False


class PollComment(Model, BaseComment):
    __tablename__ = 'poll_comment'
    
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id', ondelete='CASCADE'), index=True)
    post = db.relationship('Poll', lazy=True) 
    favorites = db.relationship("PollCommentFavorite", cascade='all,delete-orphan')
    @aggregated('favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')  

    @property
    def is_favorited_by_me(self):
        PollCommentFavorite = db.get_model('PollCommentFavorite')
        if g.current_user:
            favorite = PollCommentFavorite.query.filter(PollCommentFavorite.user_id == g.current_user.id, PollCommentFavorite.poll_comment_id == self.id).first()
            if favorite is not None:
                return True
        return False