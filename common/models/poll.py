#!/usr/bin/env python
# -*- coding: utf-8 -*-

# own modules
from common.models.mixins import AuditCreateMixin, AuditUpdateMixin
from common.db import db
from common.models.model import Model
from sqlalchemy.sql import expression

# third-party modules
from sqlalchemy_utils import aggregated
from sqlalchemy.ext.declarative import declared_attr

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class Poll(Model, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'poll'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    slug = db.Column(db.String(255), index=True)
    allow_multiple_user_select = db.Column(db.Boolean, server_default=expression.false())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True) 
    user = db.relationship('User', uselist=False, lazy=True)
    
    topics = db.relationship("Topic", secondary="poll_topic", backref='polls', lazy='subquery', uselist=True)
    fixed_topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False)
    fixed_topic = db.relationship("Topic", uselist=False, secondary="poll_topic", lazy=True)

    expire_after_seconds = db.Column(db.Integer, server_default="86400") # 1 day
    is_expire = db.Column(db.Boolean, server_default=expression.false())
    
    allow_voting = db.Column(db.Boolean, server_default=expression.true())
    allow_comments = db.Column(db.Boolean, server_default=expression.true())
    is_anonymous = db.Column(db.Boolean, server_default=expression.false())

    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def upvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'UPVOTED'"), 1, 0)), 0)

    @aggregated('votes', db.Column(db.Integer, server_default="0", nullable=False))
    def downvote_count(self):
        return db.func.coalesce(db.func.sum(db.func.if_(db.text("vote_status = 'DOWNVOTED'"), 1, 0)), 0)

    @aggregated('poll_shares', db.Column(db.Integer, server_default="0", nullable=False))
    def share_count(self):
        return db.func.count('1')
    
    @aggregated('poll_favorites', db.Column(db.Integer, server_default="0", nullable=False))
    def favorite_count(self):
        return db.func.count('1')
    
    @aggregated('poll_comments', db.Column(db.Integer, server_default="0", nullable=False))
    def comment_count(self):
        return db.func.count('1')

    @aggregated('poll_selects', db.Column(db.Integer, server_default="0",  nullable=False))
    def select_count(self):
        return db.func.count('1')

    @declared_attr
    def fixed_topic(cls):
        return db.relationship('Topic', lazy=True)

    votes = db.relationship("PollVote", cascade='all,delete-orphan')
    poll_comments = db.relationship("PollComment", cascade='all,delete-orphan', primaryjoin="and_(Poll.id == remote(PollComment.poll_id), remote(PollComment.user_id) == User.id, remote(User.is_deactivated) == False)")
    poll_shares = db.relationship("PollShare", cascade='all,delete-orphan')
    poll_favorites = db.relationship("PollFavorite", cascade='all,delete-orphan')
    poll_selects = db.relationship("PollSelect", cascade='all,delete-orphan')

    @property
    def is_bookmarked_by_me(self):
        PollBookmark = db.get_model('PollBookmark')
        if g.current_user:
            bookmark = PollBookmark.query.filter(PollBookmark.user_id == g.current_user.id,
                                            PollBookmark.poll_id == self.id).first()
            return True if bookmark else False
        return False


class PollTopic(Model, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'poll_topic'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id', ondelete='CASCADE'), nullable=False, index=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)
    topic = db.relationship('Topic', uselist=False, lazy=True)
    poll = db.relationship('Poll', uselist=False, lazy=True)


class PollSelect(Model, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'poll_select'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id', ondelete='CASCADE'), nullable=False, index=True)
    poll = db.relationship('Poll', uselist=False, lazy=True)
    poll_user_selects = db.relationship('PollUserSelect', lazy=True)
    content = db.Column(db.UnicodeText, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User', uselist=False, lazy=True)

    @aggregated('poll_user_selects', db.Column(db.Integer))
    def select_count(self):
        return db.func.count('1')


class PollUserSelect(Model, AuditCreateMixin, AuditUpdateMixin):
    __tablename__ = 'poll_user_select'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User',uselist=False, lazy=True)
    poll_select = db.relationship('PollSelect', uselist=False, lazy=True)
    poll_select_id = db.Column(db.Integer, db.ForeignKey('poll_select.id', ondelete='CASCADE'), nullable=False, index=True)
