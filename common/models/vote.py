#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.ext.declarative import declared_attr

# own modules
from common.db import db
from common.enum import VotingStatusEnum
from common.models.model import Model
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class BaseVote(OrganizationRole):
    id = db.Column(db.Integer, primary_key=True)
    vote_status = db.Column(db.Enum(VotingStatusEnum, validate_strings=True), nullable=False, server_default="NEUTRAL")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)

    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class QuestionVote(Model, BaseVote):
    __tablename__ = 'question_vote'
    
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), index=True)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question


class AnswerVote(Model, BaseVote):
    __tablename__ = 'answer_vote'
    
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), index=True)
    answer =  db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer


class AnswerImprovementVote(Model, BaseVote):
    __tablename__ = 'answer_improvement_vote'
    
    improvement_id = db.Column(db.Integer, db.ForeignKey('answer_improvement.id', ondelete='CASCADE'), index=True)
    improvement =  db.relationship('AnswerImprovement', lazy=True) # one-to-many relationship with table Answer

class ArticleVote(Model, BaseVote):
    __tablename__ = 'article_vote'

    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), index=True)
    article = db.relationship('Article', lazy=True) # one-to-many relationship with table Article

class PollVote(Model, BaseVote):
    __tablename__ = 'poll_vote'

    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id', ondelete='CASCADE'), index=True)
    poll = db.relationship('Poll', lazy=True) # one-to-many relationship with table Poll