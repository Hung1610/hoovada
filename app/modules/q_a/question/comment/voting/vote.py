#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum

# own modules
from app import db
from app.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class VotingStatusEnum(enum.Enum):
    NEUTRAL = 1
    UPVOTED = 2
    DOWNVOTED = 3


class QuestionCommentVote(Model):
    __tablename__ = 'question_comment_vote'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer, db.ForeignKey('question_comment.id'))
    comment = db.relationship('QuestionComment', lazy=True) # one-to-many relationship with table Comment
    vote_status = db.Column(db.Enum(VotingStatusEnum, validate_strings=True), nullable=False, server_default="NEUTRAL")
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)