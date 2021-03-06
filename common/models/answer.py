#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

#third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from flask import g

# own modules
from common.enum import VotingStatusEnum
from common.models.mixins import AnonymousMixin, AuditCreateMixin, AuditUpdateMixin, SoftDeleteMixin
from common.db import db
from common.enum import FileTypeEnum, EntityTypeEnum
from common.models.model import Model
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

class Answer(Model, SoftDeleteMixin, AuditCreateMixin, AuditUpdateMixin, AnonymousMixin, OrganizationRole):
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
    allow_voting = db.Column(db.Boolean, server_default=expression.true())
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

    user_education_id = db.Column(db.Integer, db.ForeignKey('user_education.id', ondelete='CASCADE'), nullable=True, index=True)
    user_education = db.relationship('UserEducation', lazy=True) # one-to-many relationship with table UserEducation
    user_location_id = db.Column(db.Integer, db.ForeignKey('user_location.id', ondelete='CASCADE'), nullable=True, index=True)
    user_location = db.relationship('UserLocation', uselist=False, lazy=True)
    user_employment_id = db.Column(db.Integer, db.ForeignKey('user_employment.id', ondelete='CASCADE'), nullable=True, index=True)
    user_employment = db.relationship('UserEmployment', uselist=False, lazy=True)
    user_language_id = db.Column(db.Integer, db.ForeignKey('user_language.id', ondelete='CASCADE'), nullable=True, index=True)
    user_language = db.relationship('UserLanguage', uselist=False, lazy=True)
    user_topic_id = db.Column(db.Integer, db.ForeignKey('user_topic.id', ondelete='CASCADE'), nullable=True, index=True)
    user_topic = db.relationship('UserTopic', uselist=False, lazy=True)

    votes = db.relationship("AnswerVote", cascade='all,delete-orphan')
    answer_shares = db.relationship("AnswerShare", cascade='all,delete-orphan')
    answer_reports = db.relationship("AnswerReport", cascade='all,delete-orphan')
    answer_favorites = db.relationship("AnswerFavorite", cascade='all,delete-orphan')
    answer_bookmarks = db.relationship("AnswerBookmark", cascade='all,delete-orphan')
    answer_comments = db.relationship("AnswerComment", cascade='all,delete-orphan', primaryjoin="and_(Answer.id == remote(AnswerComment.answer_id),\
                        remote(AnswerComment.user_id) == User.id, remote(User.is_deactivated) == False)")

    @property
    def is_bookmarked_by_me(self):
        AnswerBookmark = db.get_model('AnswerBookmark')
        if g.current_user:
            bookmark = AnswerBookmark.query.filter(AnswerBookmark.user_id == g.current_user.id, AnswerBookmark.answer_id == self.id).first()
            return True if bookmark else False
        return False

    @property
    def is_upvoted_by_me(self):
        AnswerVote = db.get_model('AnswerVote')
        if g.current_user:
            vote = AnswerVote.query.filter(AnswerVote.user_id == g.current_user.id, AnswerVote.answer_id == self.id).first()
            return True if VotingStatusEnum(2).name == vote.vote_status.name else False
        return False

    @property
    def is_downvoted_by_me(self):
        AnswerVote = db.get_model('AnswerVote')
        if g.current_user:
            vote = AnswerVote.query.filter(AnswerVote.user_id == g.current_user.id, AnswerVote.answer_id == self.id).first()
            return True if VotingStatusEnum(3).name == vote.vote_status.name else False
        return False


class AnswerImprovement(Model, AuditCreateMixin, AuditUpdateMixin, OrganizationRole):
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
