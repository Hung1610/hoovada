#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from slugify import slugify

# third-party modules
from sqlalchemy_utils import aggregated
from sqlalchemy.sql import expression
from sqlalchemy import event

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicUserEndorse(Model):
    __tablename__ = 'topic_user_endorse'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    endorsed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Topic

class Topic(Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255), index=True)
    count = db.Column(db.Integer, default=0) # chua ro truong nay su dung lam gi
    user_id = db.Column(db.Integer)  # who created this topic
    color_code = db.Column(db.String(100))
    file_url = db.Column(db.String(255))
    # question_count = db.Column(db.Integer, default=0)  # amount of question related to this topic
    questions = db.relationship('Question', lazy='dynamic')
    @aggregated('questions', db.Column(db.Integer))
    def question_count(self):
        return db.func.count('1')
    user_count = db.Column(db.Integer, default=0)  # Number of users who interest this topic
    answer_count = db.Column(db.Integer, default=0)  # how many answers related to this topic
    parent_id = db.Column(db.Integer, db.ForeignKey('topic.id'))  # the ID of parent topic
    children = db.relationship("Topic", cascade='all,delete-orphan')
    parent = db.relationship("Topic", remote_side=[id], lazy=True)
    is_fixed = db.Column(db.Boolean, default=False)  # is this topic fixed?
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))
    is_nsfw = db.Column(db.Boolean, server_default=expression.false())  # is this topic fixed?
    endorsed_users = db.relationship('User', secondary='topic_user_endorse', foreign_keys=[TopicUserEndorse.user_id, TopicUserEndorse.topic_id], lazy='dynamic')
    fixed_topic_articles = db.relationship("Article", cascade='all,delete-orphan')
    avatar = db.Column(db.String(255))

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            if target.parent:
                target.slug = '{}-{}'.format(slugify(target.parent.name), slugify(value))
            else:
                target.slug = '{}'.format(slugify(value))

event.listen(Topic.name, 'set', Topic.generate_slug, retval=False)