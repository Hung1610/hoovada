#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import g
from sqlalchemy.orm import backref
from sqlalchemy.sql import expression
from sqlalchemy_utils import aggregated
from werkzeug.security import check_password_hash, generate_password_hash

# own modules
from common.db import db
from common.enum import FrequencySettingEnum
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
    user_id = db.Column(db.Integer, index=True)


class User(Model):
    """
    Define the User model.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.Unicode(255), unique=True, nullable=False, index=True)  # , default='')
    phone_number = db.Column(db.String(255), unique=True, nullable=True)
    verification_sms_time = db.Column(db.DateTime, default=datetime.utcnow)

    first_name = db.Column(db.Unicode(255))  # (128), default='')
    middle_name = db.Column(db.Unicode(255))  # (128), default='')
    last_name = db.Column(db.Unicode(255))  # (128), default='')

    gender = db.Column(db.String(255))  # (10), default='')
    age = db.Column(db.String(255))  # (3), default='')
    birthday = db.Column(db.DateTime)
    is_birthday_hidden = db.Column(db.Boolean, server_default=expression.false())
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

    about_me = db.Column(db.Text, default='')

    document_pic_url = db.Column(db.String(255)) 
    verified_document = db.Column(db.Boolean, default=False) 
    
    # Settings
    show_email_publicly_setting = db.Column(db.Boolean, default=False)
    hoovada_digests_setting = db.Column(db.Boolean, default=True)
    hoovada_digests_frequency_setting = db.Column(db.Enum(FrequencySettingEnum, validate_strings=True), nullable=False, server_default='weekly')

    new_answer_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    new_answer_email_settings = db.Column(db.Boolean, server_default=expression.true())

    my_question_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    my_question_email_settings = db.Column(db.Boolean, server_default=expression.true())
    
    new_question_comment_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    new_question_comment_email_settings = db.Column(db.Boolean, server_default=expression.true())

    new_answer_comment_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    new_answer_comment_email_settings = db.Column(db.Boolean, server_default=expression.true())

    new_article_comment_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    new_article_comment_email_settings = db.Column(db.Boolean, server_default=expression.true())

    question_invite_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    question_invite_email_settings = db.Column(db.Boolean, server_default=expression.true())

    friend_request_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    friend_request_email_settings = db.Column(db.Boolean, server_default=expression.true())

    follow_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    follow_email_settings = db.Column(db.Boolean, server_default=expression.true())

    followed_new_publication_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    followed_new_publication_email_settings = db.Column(db.Boolean, server_default=expression.true())

    admin_interaction_notify_settings = db.Column(db.Boolean, server_default=expression.true())
    admin_interaction_email_settings = db.Column(db.Boolean, server_default=expression.true())

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
    def article_aggregated_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1') & db.text('is_anonymous <> 1'), 1, 0))
    @property
    def article_count(self):
        if g.current_user and g.current_user.id == self.id:
            Article = db.get_model('Article')
            anonymous_count = Article.query.with_entities(db.func.count(Article.id)).filter(\
                                                (Article.user_id == self.id) &
                                                (Article.is_deleted != True) &
                                                (Article.is_anonymous == True)).scalar()
            return self.article_aggregated_count + anonymous_count
        return self.article_aggregated_count

    answers = db.relationship("Answer", cascade='all,delete-orphan')
    @aggregated('answers', db.Column(db.Integer))
    def answer_aggregated_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1') & db.text('is_anonymous <> 1'), 1, 0))
    @property
    def answer_count(self):
        if g.current_user and g.current_user.id == self.id:
            Answer = db.get_model('Answer')
            anonymous_count = Answer.query.with_entities(db.func.count(Answer.id)).filter(\
                                                (Answer.user_id == self.id) &
                                                (Answer.is_deleted != True) &
                                                (Answer.is_anonymous == True)).scalar()
            return self.answer_aggregated_count + anonymous_count
        return self.answer_aggregated_count
    
    questions = db.relationship("Question", cascade='all,delete-orphan')
    @aggregated('questions', db.Column(db.Integer))
    def question_aggregated_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1') & db.text('is_anonymous <> 1'), 1, 0))
    @property
    def question_count(self):
        if g.current_user and g.current_user.id == self.id:
            Question = db.get_model('Question')
            anonymous_count = Question.query.with_entities(db.func.count(Question.id)).filter(\
                                                (Question.user_id == self.id) &
                                                (Question.is_deleted != True) &
                                                (Question.is_anonymous == True)).scalar()
            return self.question_aggregated_count + anonymous_count
        return self.question_aggregated_count
    
    posts = db.relationship("Post", cascade='all,delete-orphan')
    @aggregated('posts', db.Column(db.Integer))
    def post_count(self):
        return db.func.sum(db.func.if_(db.text('is_deleted <> 1'), 1, 0))
    
    timelines = db.relationship("Timeline", cascade='all,delete-orphan')
    
    user_educations = db.relationship("UserEducation", cascade='all,delete-orphan')
    user_locations = db.relationship("UserLocation", cascade='all,delete-orphan')
    
    languages = db.relationship("Language", secondary='user_language')
    @aggregated('sent_friend_requests', db.Column(db.Integer))
    def friends_sent_count(self):
        return db.func.count('1')
    @aggregated('received_friend_requests', db.Column(db.Integer))
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
        try:
            TopicUserEndorse = db.get_model('TopicUserEndorse')
            if g.endorsed_topic_id:
                endorsed_count = TopicUserEndorse.query.with_entities(TopicUserEndorse.id).filter(TopicUserEndorse.endorsed_id == self.id,
                                                TopicUserEndorse.topic_id == g.endorsed_topic_id).count()
                return endorsed_count
            return 0
        except Exception as e:
            print(e)

    @property
    def is_approved_friend(self):
        UserFriend = db.get_model('UserFriend')
        if g.current_user:
            friend = UserFriend.query.with_entities(UserFriend.id).filter(\
                                                ((UserFriend.friended_id ==g.current_user.id) & (UserFriend.friend_id == self.id)) |
                                                ((UserFriend.friend_id ==g.current_user.id) & (UserFriend.friended_id == self.id))
                                            ).first()
            return True if friend else False
        return False

    @property
    def is_friend_requested(self):
        UserFriend = db.get_model('UserFriend')
        if g.current_user:
            friend = UserFriend.query.with_entities(UserFriend.id).filter(UserFriend.friend_id == self.id,
                                             UserFriend.friended_id == g.current_user.id).first()
            return True if friend else False
        return False

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

    @property
    def is_facebook_linked(self):
        SocialAccount = db.get_model('SocialAccount')
        social_account = SocialAccount.query.with_entities(SocialAccount.id).filter(
                (SocialAccount.user_id == self.id) & (SocialAccount.provider == 'facebook')
            ).first()
        return True if social_account else False

    @property
    def is_google_linked(self):
        SocialAccount = db.get_model('SocialAccount')
        social_account = SocialAccount.query.with_entities(SocialAccount.id).filter(
                (SocialAccount.user_id == self.id) & (SocialAccount.provider == 'google')
            ).first()
        return True if social_account else False

class UserLocation(Model):
    __tablename__ = 'user_location'

    id = db.Column(db.Integer, primary_key=True)
    location_detail = db.Column(db.UnicodeText)
    is_current = db.Column(db.Boolean, default=False)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserLanguage(Model):
    __tablename__ = 'user_language'

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False, index=True)
    language = db.relationship('Language', lazy=True) # one-to-many relationship with table Article
    level = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    is_default = db.Column(db.Boolean, default=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserEducation(Model):
    __tablename__ = 'user_education'

    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.UnicodeText)
    primary_major = db.Column(db.UnicodeText)
    secondary_major = db.Column(db.UnicodeText)
    is_current = db.Column(db.Boolean, default=False)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserEmployment(Model):
    __tablename__ = 'user_employment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    position = db.Column(db.String(255))
    company = db.Column(db.String(255))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    is_current = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserPermission(Model):
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), index=True)
    permission_id = db.Column(db.ForeignKey('permission.id'), index=True)
    allow = db.Column(db.Boolean, default=False)


class UserTopic(Model):
    __tablename__ = 'user_topic'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False, index=True)
    topic = db.relationship('Topic', foreign_keys=[topic_id], lazy=True) # one-to-many relationship with table Article
    description = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    user = db.relationship('User', lazy=True) # one-to-many relationship with table Article
    is_default = db.Column(db.Boolean, default=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserSeenQuestion(Model):
    """
    Define the questions that the user has seen.
    """
    __tablename__ = 'user_seen_question'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=backref("seen_question_users", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True, index=True)
    question = db.relationship('Question', backref=backref("seen_items", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserSeenArticle(Model):
    """
    Define the articles that the user has seen.
    """
    __tablename__ = 'user_seen_article'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=backref("seen_article_users", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=True, index=True)
    article = db.relationship('Article', backref=backref("seen_items", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserMailedQuestion(Model):
    """
    Define the questions that the user has been mailed.
    Used to keep track of recommendation mailing tasks.
    """
    __tablename__ = 'user_mailed_question'

    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=backref("mailed_question_users", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True, index=True)
    question = db.relationship('Question', backref=backref("mailed_items", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class UserMailedArticle(Model):
    """
    Define the articles that the user has been mailed.
    Used to keep track of recommendation mailing tasks.
    """
    __tablename__ = 'user_mailed_article'

    def __init__(self, user_id, article_id):
        self.user_id = user_id
        self.article_id = article_id

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=backref("mailed_article_users", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=True, index=True)
    article = db.relationship('Article', backref=backref("mailed_items", cascade="all, delete-orphan"), lazy=True) # one-to-many relationship with table Post
    created_date = db.Column(db.DateTime, default=datetime.utcnow)