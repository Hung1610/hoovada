#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from app import db
from app.modules.common.model import Model

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# topic_questions = db.Table('question_topic',
#     db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True),
#     db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
#     db.Column('created_date', db.DateTime, default=datetime.utcnow),
# )

question_user_invite = db.Table('question_user_invite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
)

class Question(Model):
    __tablename__ = 'question'
    __table_args__ = (
        db.Index("idx_question_title", "title", mysql_length=255),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer)
    question_by_user = db.relationship('User', backref='questions', lazy=True) # one-to-many relationship with table User
    fixed_topic_id = db.Column(db.Integer)
    fixed_topic = db.relationship('Topic', backref='fixed_topic_questions', lazy=True) # one-to-many relationship with table Article
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
    
    # @aggregated('votes', db.Column(db.Integer))
    # def upvote_count(self):
    #     return db.func.sum(db.func.if_(ArticleVote.vote_status == 'UPVOTED', 1, 0))
    # @aggregated('votes', db.Column(db.Integer))
    # def downvote_count(self):
    #     return db.func.sum(db.func.if_(ArticleVote.vote_status == 'DOWNVOTED', 1, 0))
    # @aggregated('shares', db.Column(db.Integer))
    # def share_count(self):
    #     return db.func.count('1')
    # @aggregated('article_favorites', db.Column(db.Integer))
    # def favorite_count(self):
    #     return db.func.count('1')

    slug = db.Column(db.UnicodeText)
    allow_video_answer = db.Column(db.Boolean, server_default=expression.true())
    allow_audio_answer = db.Column(db.Boolean, server_default=expression.true())
    is_private = db.Column(db.Boolean, default=False)
    topics = db.relationship('Topic', secondary='question_topic', lazy='subquery', backref=db.backref('questions', lazy=True))
    invited_users = db.relationship('User', secondary='question_user_invite', lazy='subquery', backref=db.backref('invited_to_questions', lazy=True))


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
    slug = db.Column(db.UnicodeText)
    allow_video_answer = db.Column(db.Boolean, default=True)
    allow_audio_answer = db.Column(db.Boolean, default=True)
    is_private = db.Column(db.Boolean, default=False)