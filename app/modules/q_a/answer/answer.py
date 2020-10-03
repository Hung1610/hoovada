#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum
from datetime import datetime

#third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from app import db
from app.modules.common.model import Model
from app.modules.q_a.answer.voting.vote import AnswerVote

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class FileTypeEnum(enum.Enum):
    AUDIO = 1
    VIDEO = 2

class Answer(Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    accepted = db.Column(db.Boolean, default=False)
    answer = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', lazy=True) # one-to-many relationship with table Question
    image_ids = db.Column(db.JSON)
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    allow_improvement = db.Column(db.Boolean, server_default=expression.true())
    file_url = db.Column(db.String(255))
    file_type = db.Column(db.Enum(FileTypeEnum, validate_strings=True), nullable=True)

    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.sum(db.func.if_(AnswerVote.vote_status == 'UPVOTED', 1, 0))

    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.sum(db.func.if_(AnswerVote.vote_status == 'DOWNVOTED', 1, 0))

    @aggregated('answer_comments', db.Column(db.Integer))
    def comment_count(self):
        return db.func.count('1')

    @aggregated('answer_shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')

    @aggregated('answer_favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')

    votes = db.relationship("AnswerVote", cascade='all,delete-orphan')
    answer_shares = db.relationship("AnswerShare", cascade='all,delete-orphan')
    answer_reports = db.relationship("AnswerReport", cascade='all,delete-orphan')
    answer_favorites = db.relationship("AnswerFavorite", cascade='all,delete-orphan')
    answer_bookmarks = db.relationship("AnswerBookmark", cascade='all,delete-orphan')
    answer_comments = db.relationship("AnswerComment", cascade='all,delete-orphan')
    is_deleted = db.Column(db.Boolean, server_default=expression.false())
