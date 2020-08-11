#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."



class Question(Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer)
    fixed_topic_id = db.Column(db.Integer)
    fixed_topic_name = db.Column(db.String(255))
    question = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    answers_count = db.Column(db.Integer, default=0)
    accepted_answer_id = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean, default=False)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    upvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly upvote
    downvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly downvote
    share_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)


class QuestionTopicView(Model):
    __tablename__ = 'topic_question'
    __table_args__ = {'info': dict(is_view=True)}

    topic_id = db.Column(db.Integer)
    topic_name = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer)
    fixed_topic_id = db.Column(db.Integer)
    fixed_topic_name = db.Column(db.String(255))
    question = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    answers_count = db.Column(db.Integer, default=0)
    accepted_answer_id = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean, default=False)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    upvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly upvote
    downvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly downvote
    share_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)