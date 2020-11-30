#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from werkzeug.security import check_password_hash, generate_password_hash

from app.app import db
# own modules
from common.models.model import Model
from common.utils.types import UserRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


UserFollow = db.get_model('UserFollow')


class SocialAccount(Model):
    """
    Define the SocialAccount model.
    """
    __tablename__ = 'social_account'

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(30))
    uid = db.Column(db.String(200))
    last_login = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    extra_data = db.Column(db.String(500))
    user_id = db.Column(db.Integer)


class User(Model):
    """
    Define the User model.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    # display_name = db.Column(db.String(255)(128), unique=True)
    display_name = db.Column(db.String(255), unique=True, nullable=False)  # , default='')
    # title = db.Column(db.String(255)(10), default='')
    title = db.Column(db.String(255))  # , default='')

    # user_name = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), unique=True, nullable=True)
    # verification_sms_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verification_sms_time = db.Column(db.DateTime, default=datetime.utcnow)

    first_name = db.Column(db.String(255))  # (128), default='')
    middle_name = db.Column(db.String(255))  # (128), default='')
    last_name = db.Column(db.String(255))  # (128), default='')

    gender = db.Column(db.String(255))  # (10), default='')
    age = db.Column(db.String(255))  # (3), default='')
    email = db.Column(db.String(255))  # (255), unique=True)
    password_hash = db.Column(db.String(255))  # (128), default='')

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_at = db.Column(db.DateTime, nullable=True)

    profile_pic_url = db.Column(db.String(255))  # (255), default='')
    cover_pic_url = db.Column(db.String(255))  # (255), default='')
    admin = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)

    reputation = db.Column(db.Integer, server_default='0')
    profile_views = db.Column(db.Integer, server_default='0')

    # about_me = db.Column(db.String(255)(3000))
    about_me = db.Column(db.Text, default='')
    about_me_markdown = db.Column(db.Text, default='')
    about_me_html = db.Column(db.Text, default='')

    people_reached = db.Column(db.Integer, server_default='0')
    # Settings
    show_email_publicly_setting = db.Column(db.Boolean, default=False)
    hoovada_digests_setting = db.Column(db.Boolean, default=True)
    hoovada_digests_frequency_setting = db.Column(db.String(255), default='weekly')

    questions_you_asked_or_followed_setting = db.Column(db.Boolean, default=True)
    questions_you_asked_or_followed_frequency_setting = db.Column(db.String(255), default='weekly')
    people_you_follow_setting = db.Column(db.Boolean, default=True)

    people_you_follow_frequency_setting = db.Column(db.String(255), default='weekly')
    email_stories_topics_setting = db.Column(db.Boolean, default=True)
    email_stories_topics_frequency_setting = db.Column(db.String(255), default='weekly')
    last_message_read_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    question_favorite_count = db.Column(db.Integer, server_default='0')
    question_favorited_count = db.Column(db.Integer, server_default='0')
    question_share_count = db.Column(db.Integer, server_default='0')
    question_shared_count = db.Column(db.Integer, server_default='0')
    question_report_count = db.Column(db.Integer, server_default='0')
    question_reported_count = db.Column(db.Integer, server_default='0')
    question_upvote_count = db.Column(db.Integer, server_default='0')
    question_upvoted_count = db.Column(db.Integer, server_default='0')
    question_downvote_count = db.Column(db.Integer, server_default='0')
    question_downvoted_count = db.Column(db.Integer, server_default='0')

    answer_share_count = db.Column(db.Integer, server_default='0')
    answer_shared_count = db.Column(db.Integer, server_default='0')
    answer_favorite_count = db.Column(db.Integer, server_default='0')
    answer_favorited_count = db.Column(db.Integer, server_default='0')
    answer_upvote_count = db.Column(db.Integer, server_default='0')
    answer_upvoted_count = db.Column(db.Integer, server_default='0')
    answer_downvote_count = db.Column(db.Integer, server_default='0')
    answer_downvoted_count = db.Column(db.Integer, server_default='0')
    answer_report_count = db.Column(db.Integer, server_default='0')
    answer_reported_count = db.Column(db.Integer, server_default='0')

    followed_topics = db.relationship('Topic', secondary='topic_follow', lazy='dynamic')
    @aggregated('followed_topics', db.Column(db.Integer))
    def topic_followed_count(self):
        return db.func.count('1')
    created_topics = db.relationship('Topic', lazy='dynamic')
    @aggregated('created_topics', db.Column(db.Integer))
    def topic_created_count(self):
        return db.func.count('1')

    @property
    def user_follow_count(self):
        followers = UserFollow.query.with_entities(UserFollow.follower_id).filter(UserFollow.followed_id == self.id).all()
        follower_ids = [follower[0] for follower in followers]
        follower_count = User.query.with_entities(db.func.count(User.id))\
            .filter(User.id.in_(follower_ids))\
            .filter(db.text('IFNULL(is_deactivated, False) = False'))\
            .scalar()

        return follower_count

    @property
    def user_followed_count(self):
        followeds = UserFollow.query.with_entities(UserFollow.followed_id).filter(UserFollow.follower_id == self.id).all()
        followed_ids = [followed[0] for followed in followeds]
        followed_count = User.query.with_entities(db.func.count(User.id))\
            .filter(User.id.in_(followed_ids))\
            .filter(db.text('IFNULL(is_deactivated, False) = False'))\
            .scalar()

        return followed_count

    comment_count = db.Column(db.Integer, server_default='0')
    comment_upvote_count = db.Column(db.Integer, server_default='0')
    comment_upvoted_count = db.Column(db.Integer, server_default='0')
    comment_downvote_count = db.Column(db.Integer, server_default='0')
    comment_downvoted_count = db.Column(db.Integer, server_default='0')
    comment_report_count = db.Column(db.Integer, server_default='0')
    comment_reported_count = db.Column(db.Integer, server_default='0')

    user_report_count = db.Column(db.Integer, server_default='0')
    user_reported_count = db.Column(db.Integer, server_default='0')

    article_share_count = db.Column(db.Integer, server_default='0')
    article_shared_count = db.Column(db.Integer, server_default='0')

    is_deactivated = db.Column(db.Boolean, server_default=expression.false())

    is_private = db.Column(db.Boolean, server_default=expression.false())

    show_nsfw = db.Column(db.Boolean, server_default=expression.false())
    
    articles = db.relationship("Article", cascade='all,delete-orphan')
    @aggregated('articles', db.Column(db.Integer))
    def article_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1'), 1, 0))

    answers = db.relationship("Answer", cascade='all,delete-orphan')
    @aggregated('answers', db.Column(db.Integer))
    def answer_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1'), 1, 0))
    
    questions = db.relationship("Question", cascade='all,delete-orphan')
    @aggregated('questions', db.Column(db.Integer))
    def question_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1'), 1, 0))
    
    posts = db.relationship("Post", cascade='all,delete-orphan')
    @aggregated('posts', db.Column(db.Integer))
    def post_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1'), 1, 0))
    
    timelines = db.relationship("Timeline", cascade='all,delete-orphan')
    
    user_educations = db.relationship("UserEducation", cascade='all,delete-orphan')
    user_locations = db.relationship("UserLocation", cascade='all,delete-orphan')
    
    languages = db.relationship("Language", secondary='user_language')
    @aggregated('friends', db.Column(db.Integer))
    def friends_sent_count(self):
        return db.func.count('1')
    @aggregated('friend_requests', db.Column(db.Integer))
    def friend_received_count(self):
        return db.func.count('1')

        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_online(self):
        return abs(self.last_seen-datetime.now()).total_seconds() < 60

    @property
    def is_super_admin(self):
        return UserRole.is_super_admin(self.admin)

    @property
    def friend_count(self):
        UserFriend = db.get_model('UserFriend')
        friend_count = UserFriend.query.with_entities(UserFriend.id).filter(\
                                            (UserFriend.friend_id == self.id) |
                                            (UserFriend.friended_id == self.id)).count()
        return friend_count

    @property
    def is_endorsed_by_me(self):
        TopicUserEndorse = db.get_model('TopicUserEndorse')
        if g.current_user:
            if g.endorsed_topic_id:
                endorsed = TopicUserEndorse.query.with_entities(TopicUserEndorse.id).filter(TopicUserEndorse.user_id == g.current_user.id,
                                                TopicUserEndorse.endorsed_id == self.id,
                                                TopicUserEndorse.topic_id == g.endorsed_topic_id).first()
                return True if endorsed else False
            return False
        return False

    @property
    def endorsed_count(self):
        TopicUserEndorse = db.get_model('TopicUserEndorse')
        if g.endorsed_topic_id:
            endorsed_count = TopicUserEndorse.query.with_entities(TopicUserEndorse.id).filter(TopicUserEndorse.endorsed_id == self.id,
                                            TopicUserEndorse.topic_id == g.endorsed_topic_id).count()
            return endorsed_count
        return 0

    @property
    def is_friended_by_me(self):
        UserFriend = db.get_model('UserFriend')
        if g.current_user:
            friend = UserFriend.query.with_entities(UserFriend.id).filter(UserFriend.friend_id == g.current_user.id,
                                             UserFriend.friended_id == self.id).first()
            return True if friend else False
        return False

    @property
    def is_followed_by_me(self):
        UserFollow = db.get_model('UserFollow')
        if g.current_user:
            follow = UserFollow.query.with_entities(UserFollow.id).filter(UserFollow.follower_id == g.current_user.id,
                                            UserFollow.followed_id == self.id).first()
            return True if follow else False
        return False
