#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated

# own modules
from app import db
from common.models.model import Model
from app.modules.q_a.question.voting.vote import QuestionVote
from app.modules.q_a.answer.answer import Answer

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


# topic_questions = db.Table('question_topic',
#     db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True),
#     db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True),
#     db.Column('created_date', db.DateTime, default=datetime.utcnow),
# )

question_user_invite = db.Table('question_user_invite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True),
)

question_proposal_topics = db.Table('question_proposal_topic',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('question_proposal_id', db.Integer, db.ForeignKey('question_proposal.id')),
    db.Column('created_date', db.DateTime, default=datetime.utcnow),
)

question_proposal_user_invite = db.Table('question_proposal_user_invite',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('question_proposal_id', db.Integer, db.ForeignKey('question_proposal.id')),
)

class Question(Model):
    __tablename__ = 'question'
    __table_args__ = (
        db.Index("idx_question_title", "title", mysql_length=255),
        db.Index("idx_question_slug", "slug", mysql_length=255),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    slug = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    question_by_user = db.relationship('User', lazy=True) # one-to-many relationship with table User
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    fixed_topic = db.relationship('Topic', lazy=True) # one-to-many relationship with table Article
    fixed_topic_name = db.Column(db.String(255))
    question = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_answer_id = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean, default=False)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    
    @aggregated('answers', db.Column(db.Integer))
    def answers_count(self):
        return db.func.sum(db.func.if_(Answer.is_deleted != True, 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def upvote_count(self):
        return db.func.sum(db.func.if_(QuestionVote.vote_status == 'UPVOTED', 1, 0))
    @aggregated('votes', db.Column(db.Integer))
    def downvote_count(self):
        return db.func.sum(db.func.if_(QuestionVote.vote_status == 'DOWNVOTED', 1, 0))
    @aggregated('question_shares', db.Column(db.Integer))
    def share_count(self):
        return db.func.count('1')
    @aggregated('question_favorites', db.Column(db.Integer))
    def favorite_count(self):
        return db.func.count('1')
    @aggregated('question_comments', db.Column(db.Integer))
    def comment_count(self):
        return db.func.count('1')

    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    allow_video_answer = db.Column(db.Boolean, server_default=expression.false())
    allow_audio_answer = db.Column(db.Boolean, server_default=expression.false())
    is_private = db.Column(db.Boolean, server_default=expression.false())
    topics = db.relationship('Topic', secondary='question_topic', lazy='subquery')
    invited_users = db.relationship('User', secondary='question_user_invite', lazy='subquery')
    answers = db.relationship("Answer", cascade='all,delete-orphan')
    votes = db.relationship("QuestionVote", cascade='all,delete-orphan')
    question_comments = db.relationship("QuestionComment", cascade='all,delete-orphan')
    question_shares = db.relationship("QuestionShare", cascade='all,delete-orphan')
    question_reports = db.relationship("QuestionReport", cascade='all,delete-orphan')
    question_favorites = db.relationship("QuestionFavorite", cascade='all,delete-orphan')
    question_bookmarks = db.relationship("QuestionBookmark", cascade='all,delete-orphan')
    is_deleted = db.Column(db.Boolean, default=False, server_default=expression.false())

class QuestionProposal(Model):
    __tablename__ = 'question_proposal'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.UnicodeText)
    slug = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    fixed_topic_name = db.Column(db.String(255))
    question = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    html = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_answer_id = db.Column(db.Integer)
    anonymous = db.Column(db.Boolean, default=False)
    user_hidden = db.Column(db.Boolean, default=False)
    image_ids = db.Column(db.JSON)
    # upvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly upvote
    # downvote_count = db.Column(db.Integer, default=0)  # question tam thoi chua xu ly downvote
    # share_count = db.Column(db.Integer, default=0)
    # favorite_count = db.Column(db.Integer, default=0)

    allow_video_answer = db.Column(db.Boolean, server_default=expression.false())
    allow_audio_answer = db.Column(db.Boolean, server_default=expression.false())
    is_private = db.Column(db.Boolean, server_default=expression.false())
    topics = db.relationship('Topic', secondary='question_proposal_topic', lazy='subquery')
    invited_users = db.relationship('User', secondary='question_proposal_user_invite', lazy='subquery')
    proposal_created_date = db.Column(db.DateTime, default=datetime.utcnow)
    proposal_updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, server_default=expression.false())
    is_parma_delete = db.Column(db.Boolean, server_default=expression.false())
    is_approved = db.Column(db.Boolean, server_default=expression.false())

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
    hot_count = db.Column(db.Integer, default=0)
    allow_video_answer = db.Column(db.Boolean, default=True)
    allow_audio_answer = db.Column(db.Boolean, default=True)
    is_private = db.Column(db.Boolean, default=False)
