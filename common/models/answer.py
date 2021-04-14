#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

#third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from common.models.mixins import AnonymousMixin, AuditCreateMixin, AuditUpdateMixin, SoftDeleteMixin
from common.db import db
from common.enum import FileTypeEnum
from common.models.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Answer(Model, SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin, AnonymousMixin):
    __tablename__ = 'answer'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'question_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    accepted = db.Column(db.Boolean, default=False)
    answer = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False, index=True)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    allow_improvement = db.Column(db.Boolean, server_default=expression.true())
    file_url = db.Column(db.String(255))
    file_type = db.Column(db.Enum(FileTypeEnum, validate_strings=True), nullable=True)

    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def upvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'UPVOTED'"), 1, 0)), 0)

    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def downvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'DOWNVOTED'"), 1, 0)), 0)

    @aggregated('answer_comments', db.Column(db.Integer, server_default="0", nullable=False))
    def comment_count(self):
        return db.func.count('1')

    @aggregated('answer_shares', db.Column(db.Integer, server_default="0", nullable=False))
    def share_count(self):
        return db.func.count('1')

    @aggregated('answer_favorites', db.Column(db.Integer, server_default="0", nullable=False))
    def favorite_count(self):
        return db.func.count('1')

    votes = db.relationship("AnswerVote", cascade='all,delete-orphan')
    answer_shares = db.relationship("AnswerShare", cascade='all,delete-orphan')
    answer_reports = db.relationship("AnswerReport", cascade='all,delete-orphan')
    answer_favorites = db.relationship("AnswerFavorite", cascade='all,delete-orphan')
    answer_bookmarks = db.relationship("AnswerBookmark", cascade='all,delete-orphan')
    answer_comments = db.relationship("AnswerComment", cascade='all,delete-orphan', primaryjoin="and_(Answer.id == remote(AnswerComment.answer_id),\
                        remote(AnswerComment.user_id) == User.id, remote(User.is_deactivated) == False)")


class AnswerImprovement(Model):
    __tablename__ = 'answer_improvement'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True, index=True)
    answer = db.relationship('Answer', lazy=True) # one-to-many relationship with table Answer

    votes = db.relationship("AnswerImprovementVote", cascade='all,delete-orphan')

    @aggregated('votes', db.Column(db.Integer))
    def vote_score(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'UPVOTED'"), 1, 0)), 0)\
            - db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'DOWNVOTED'"), 1, 0)), 0)
