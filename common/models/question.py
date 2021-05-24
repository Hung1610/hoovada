#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy.sql import func
from sqlalchemy_utils import aggregated
from sqlalchemy.ext.declarative import declared_attr

# own modules
from common.db import db
from common.models.model import Model
from common.models.mixins import AnonymousMixin, AuditCreateMixin, AuditUpdateMixin, SoftDeleteMixin

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class QuestionUserInvite(Model):
    __tablename__= 'question_user_invite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    question_id = db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    status = db.Column('status', db.SmallInteger, server_default="0", comment='Determine the status of the invited question (0: unanswered, 1: answered, 2: declined)')


question_proposal_topics = db.Table('question_proposal_topic',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE')),
    db.Column('question_proposal_id', db.Integer, db.ForeignKey('question_proposal.id', ondelete='CASCADE')),
    db.Column('created_date', db.DateTime, server_default=func.now()),
)


question_topics = db.Table('question_topic',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False),
    db.Column('created_date', db.DateTime, server_default=func.now()),
)


# pylint: disable=R0201
class BaseQuestion(SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin, AnonymousMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))
    slug = db.Column(db.String(255), index=True)
    question = db.Column(db.UnicodeText)
    accepted_answer_id = db.Column(db.Integer)
    allow_voting = db.Column(db.Boolean, server_default=expression.true())
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    allow_video_answer = db.Column(db.Boolean, server_default=expression.false())
    allow_audio_answer = db.Column(db.Boolean, server_default=expression.false())
    is_private = db.Column(db.Boolean, server_default=expression.false())
    last_activity = db.Column(db.DateTime, server_default=func.now())

    @declared_attr
    def fixed_topic_id(cls):
        return db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)

    @declared_attr
    def fixed_topic(cls):
        return db.relationship('Topic', lazy=True)

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)

    @declared_attr
    def user(cls):
        return db.relationship('User', lazy=True)


class Question(Model, BaseQuestion):
    __tablename__ = 'question'

    views_count = db.Column(db.Integer, server_default="0")
    
    @aggregated('answers', db.Column(db.Integer, server_default="0", nullable=False))
    def answers_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text('IFNULL(is_deleted, False) <> True'), 1, 0)), 0)
    
    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def upvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'UPVOTED'"), 1, 0)), 0)
    
    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def downvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'DOWNVOTED'"), 1, 0)), 0)
    
    @aggregated('question_shares', db.Column(db.Integer, server_default="0", nullable=False))
    def share_count(self):
        return db.func.count('1')
    
    @aggregated('question_favorites', db.Column(db.Integer, server_default="0", nullable=False))
    def favorite_count(self):
        return db.func.count('1')
    
    @aggregated('question_comments', db.Column(db.Integer, server_default="0", nullable=False))
    def comment_count(self):
        return db.func.count('1')
    
    topics = db.relationship('Topic', secondary='question_topic', backref='questions', lazy='subquery', uselist=True)
    invited_users = db.relationship('User', secondary='question_user_invite', lazy='subquery')
    answers = db.relationship("Answer", cascade='all,delete-orphan')
    votes = db.relationship("QuestionVote", cascade='all,delete-orphan')
    question_comments = db.relationship("QuestionComment", cascade='all,delete-orphan', primaryjoin="and_(Question.id == remote(QuestionComment.question_id),remote(QuestionComment.user_id) == User.id, remote(User.is_deactivated) == False)")
    question_shares = db.relationship("QuestionShare", cascade='all,delete-orphan')
    question_reports = db.relationship("QuestionReport", cascade='all,delete-orphan')
    question_favorites = db.relationship("QuestionFavorite", cascade='all,delete-orphan')
    question_bookmarks = db.relationship("QuestionBookmark", cascade='all,delete-orphan')
    bookmarked_users = db.relationship("User", secondary='question_bookmark')


class QuestionProposal(Model, BaseQuestion):
    __tablename__ = 'question_proposal'

    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=True, index=True)
    question_id = db.Column(db.Integer, nullable=True, index=True)
    topics = db.relationship('Topic', secondary='question_proposal_topic', lazy='subquery')
    proposal_created_date = db.Column(db.DateTime, server_default=func.now())
    proposal_updated_date = db.Column(db.DateTime, server_default=func.now())
    is_parma_delete = db.Column(db.Boolean, server_default=expression.false())
    is_approved = db.Column(db.Boolean, server_default=expression.false())
