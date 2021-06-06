#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from slugify import slugify

# third-party modules
from flask import g
from sqlalchemy_utils import aggregated
from sqlalchemy import event
from sqlalchemy.sql import expression

# own modules
from common.db import db
from common.models.model import Model
from common.enum import EntityTypeEnum
from common.models.organization import OrganizationRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicUserEndorse(Model):
    __tablename__ = 'topic_user_endorse'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship("User", foreign_keys=[user_id], lazy=True)
    endorsed_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    endorsed = db.relationship("User", foreign_keys=[endorsed_id], lazy=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic


class Topic(Model, OrganizationRole):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    color_code = db.Column(db.String(100))
    file_url = db.Column(db.String(255))
    fixed_topic_questions = db.relationship('Question', lazy='dynamic')
    @aggregated('questions', db.Column(db.Integer))
    def question_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text('IFNULL(is_deleted, False) <> True'), 1, 0)), 0)
    fixed_topic_articles = db.relationship('Article', lazy='dynamic')
    @aggregated('articles', db.Column(db.Integer))
    def article_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text('IFNULL(is_deleted, False) <> True'), 1, 0)), 0)
    parent_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), index=True)  # the ID of parent topic
    children = db.relationship("Topic", cascade='all,delete-orphan')
    parent = db.relationship("Topic", remote_side=[id], lazy=True)
    is_fixed = db.Column(db.Boolean, default=False)  # is this topic fixed?
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    is_nsfw = db.Column(db.Boolean, server_default=expression.false(), default=False)  # is this topic nsfw?
    endorsed_users = db.relationship('User', secondary='topic_user_endorse', foreign_keys=[TopicUserEndorse.endorsed_id, TopicUserEndorse.topic_id], lazy='dynamic')
    allow_follow = db.Column(db.Boolean, server_default=expression.true())

    @aggregated('endorsed_users', db.Column(db.Integer))
    def endorsers_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text('IFNULL(is_deactivated, False) <> True'), 1, 0)), 0)
    
    bookmarked_users = db.relationship('User', secondary='topic_bookmark', lazy='dynamic')
    @aggregated('bookmarked_users', db.Column(db.Integer))
    def bookmarkers_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text('IFNULL(is_deactivated, False) <> True'), 1, 0)), 0)

    @property
    def is_bookmarked_by_me(self):
        TopicBookmark = db.get_model('TopicBookmark')
        if g.current_user:
            bookmark = TopicBookmark.query.filter(TopicBookmark.user_id == g.current_user.id, TopicBookmark.topic_id == self.id).first()
            return True if bookmark else False
        return False


    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = '{}'.format(slugify(value))

event.listen(Topic.name, 'set', Topic.generate_slug, retval=False)