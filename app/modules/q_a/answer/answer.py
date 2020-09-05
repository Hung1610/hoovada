#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum
from datetime import datetime

#third-party modules
from sqlalchemy.sql import expression

# own modules
from app import db
from app.modules.common.model import Model

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
    upvote_count = db.Column(db.Integer, default=0)
    downvote_count = db.Column(db.Integer, default=0)
    anonymous = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean, default=False)
    answer = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='answers', lazy=True) # one-to-many relationship with table User
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    question = db.relationship('Question', backref='answers', lazy=True) # one-to-many relationship with table Question
    image_ids = db.Column(db.JSON)
    user_hidden = db.Column(db.Boolean, default=False)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    allow_improvement = db.Column(db.Boolean, server_default=expression.true())
    file_url = db.Column(db.String(255))
    file_type = db.Column(db.Enum(FileTypeEnum, validate_strings=True), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
