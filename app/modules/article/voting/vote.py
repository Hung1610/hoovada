#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import enum

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class VotingStatusEnum(enum.Enum):
    NEUTRAL = 1
    UPVOTED = 2
    DOWNVOTED = 3


class ArticleVote(Model):
    __tablename__ = 'article_vote'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    voted_article =  db.relationship('Article', backref='votes', lazy=True) # one-to-many relationship with table Article
    comment_id = db.Column(db.Integer)
    vote_status = db.Column(db.Enum(VotingStatusEnum, validate_strings=True), \
        nullable=False, server_default="NEUTRAL")
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)