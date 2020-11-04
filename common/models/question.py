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
from common.enum import ReportTypeEnum, VotingStatusEnum
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


question_user_invite = db.Table('question_user_invite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True),
)

question_proposal_topics = db.Table('question_proposal_topic',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('question_proposal_id', db.Integer, db.ForeignKey('question_proposal.id')),
    db.Column('created_date', db.DateTime, default=datetime.utcnow),
)

question_topics = db.Table('question_topic',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), nullable=False),
    db.Column('created_date', db.DateTime, default=datetime.utcnow),
)

# pylint: disable=R0201
class BaseQuestion(object):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    slug = db.Column(db.String(255))
    question = db.Column(db.UnicodeText)
    accepted_answer_id = db.Column(db.Integer)
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    allow_video_answer = db.Column(db.Boolean, server_default=expression.false())
    allow_audio_answer = db.Column(db.Boolean, server_default=expression.false())
    is_private = db.Column(db.Boolean, server_default=expression.false())
    is_deleted = db.Column(db.Boolean, default=False, server_default=expression.false())
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    @declared_attr
    def fixed_topic_id(cls):
        return db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

    @declared_attr
    def fixed_topic(cls):
        return db.relationship('Topic', lazy=True)
    
    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)

class Question(Model, BaseQuestion):
    __tablename__ = 'question'
    __table_args__ = (
        db.Index("idx_question_title", "title", mysql_length=255),
        db.Index("idx_question_slug", "slug", mysql_length=255),
    )
    
    views_count = db.Column(db.Integer, default=0)
    @aggregated('answers', db.Column(db.Integer))
    def answers_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> True'), 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.sum(db.func.if_(db.text("vote_status = 'UPVOTED'"), 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.sum(db.func.if_(db.text("vote_status = 'DOWNVOTED'"), 1, 0))
    @aggregated('question_shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')
    @aggregated('question_favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')
    @aggregated('question_comments', db.Column(db.Integer))
    def comment_count(self):
        return db.func.count('1')
    topics = db.relationship('Topic', secondary='question_topic', lazy='subquery')
    invited_users = db.relationship('User', secondary='question_user_invite', lazy='subquery')
    answers = db.relationship("Answer", cascade='all,delete-orphan')
    votes = db.relationship("QuestionVote", cascade='all,delete-orphan')
    question_comments = db.relationship("QuestionComment", cascade='all,delete-orphan')
    question_shares = db.relationship("QuestionShare", cascade='all,delete-orphan')
    question_reports = db.relationship("QuestionReport", cascade='all,delete-orphan')
    question_favorites = db.relationship("QuestionFavorite", cascade='all,delete-orphan')
    question_bookmarks = db.relationship("QuestionBookmark", cascade='all,delete-orphan')


class QuestionProposal(Model, BaseQuestion):
    __tablename__ = 'question_proposal'
    
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True)
    question_id = db.Column(db.Integer, nullable=True)
    topics = db.relationship('Topic', secondary='question_proposal_topic', lazy='subquery')
    proposal_created_date = db.Column(db.DateTime, default=datetime.utcnow)
    proposal_updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_parma_delete = db.Column(db.Boolean, server_default=expression.false())
    is_approved = db.Column(db.Boolean, server_default=expression.false())
