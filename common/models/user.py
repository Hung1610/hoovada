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

UserFollow = get_model('UserFollow')


class SocialAccount(Model):
    """
    Define the SocialAccount model.
    """
    __tablename__ = 'social_account'

    id = Column(Integer, primary_key=True)
    provider = Column(String(30))
    uid = Column(String(200))
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_joined = Column(DateTime, default=datetime.utcnow)
    extra_data = Column(String(500))
    user_id = Column(Integer, index=True)


class User(Model):
    """
    Define the User model.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    display_name = Column(Unicode(255), unique=True, nullable=False, index=True)  # , default='')
    phone_number = Column(String(255), unique=True, nullable=True)
    verification_sms_time = Column(DateTime, default=datetime.utcnow)
    first_name = Column(Unicode(255))  # (128), default='')
    middle_name = Column(Unicode(255))  # (128), default='')
    last_name = Column(Unicode(255))  # (128), default='')
    gender = Column(String(255))  # (10), default='')
    age = Column(String(255))  # (3), default='')
    birthday = Column(DateTime)
    about_me = Column(Text, default='')
    email = Column(String(255))  # (255), unique=True)
    password_hash = Column(String(255))  # (128), default='')
    last_seen = Column(DateTime, default=datetime.utcnow)
    joined_date = Column(DateTime, default=datetime.utcnow)
    email_confirmed_at = Column(DateTime, nullable=True)
    profile_pic_url = Column(String(255))  # (255), default='')
    cover_pic_url = Column(String(255))  # (255), default='')
    document_pic_url = Column(String(255))
    last_message_read_time = Column(DateTime, default=datetime.utcnow)
    reputation = Column(Integer, server_default='0', nullable=False)
    profile_views = Column(Integer, server_default='0', nullable=False)
        
    show_nsfw = Column(Boolean, server_default=expression.false(), nullable=False)
    is_deactivated = Column(Boolean, server_default=expression.false(), nullable=False)
    is_private = Column(Boolean, server_default=expression.false(), nullable=False)
    is_first_log_in = Column(Boolean, server_default=expression.false(), nullable=False)
    confirmed = Column(Boolean, server_default=expression.false(), nullable=False)
    is_birthday_hidden = Column(Boolean, server_default=expression.false(), nullable=False)
    admin = Column(Boolean, server_default=expression.false(), nullable=False)
    verified_document = Column(Boolean, server_default=expression.false(), nullable=False)
    show_fullname_instead_of_display_name = Column(Boolean, server_default=expression.false(), nullable=False)

    # these fields are deprecated, set false by default
    new_answer_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    new_answer_email_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    my_question_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    my_question_email_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    new_question_comment_notify_settings = Column(Boolean, server_default=expression.false())
    new_question_comment_email_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    new_answer_comment_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    new_answer_comment_email_settings = Column(Boolean,  server_default=expression.false(), nullable=False)
    new_article_comment_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    new_article_comment_email_settings = Column(Boolean,server_default=expression.false(), nullable=False)
    question_invite_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    question_invite_email_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    follow_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    follow_email_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    followed_new_publication_notify_settings = Column(Boolean, server_default=expression.false(), nullable=False)
    followed_new_publication_email_settings = Column(Boolean, server_default=expression.false(), nullable=False)

    friend_request_notify_settings = Column(Boolean, server_default=expression.true(), nullable=False)
    friend_request_email_settings = Column(Boolean, server_default=expression.true(), nullable=False)
    admin_interaction_notify_settings = Column(Boolean, server_default=expression.true(), nullable=False)
    admin_interaction_email_settings = Column(Boolean, server_default=expression.true(), nullable=False)

    show_email_publicly_setting = Column(Boolean, server_default=expression.false(),  nullable=False)
    hoovada_digests_setting = Column(Boolean, server_default=expression.true(),  nullable=False)
    hoovada_digests_frequency_setting = Column(Enum(FrequencySettingEnum, validate_strings=True), nullable=False, server_default='weekly')


    questions = relationship("Question", cascade='all,delete-orphan')
    @aggregated('questions', Column(Integer, server_default="0", nullable=False))
    def question_aggregated_count(self):
        return func.coalesce(
            func.sum(func.if_(text('is_anonymous <> 1'), 1, 0)), 0)

    @property
    def question_count(self):
        if self.question_aggregated_count is None:
            self.question_aggregated_count = 0
        if g.current_user and g.current_user.id == self.id:
            Question = get_model('Question')
            anonymous_count = Question.query.with_entities(func.count(Question.id)).filter( \
                (Question.user_id == self.id) &
                (Question.is_deleted != True) &
                (Question.is_anonymous == True)).scalar()
            return self.question_aggregated_count + anonymous_count
        return self.question_aggregated_count
    question_share_count = Column(Integer, server_default='0', nullable=False)
    question_shared_count = Column(Integer, server_default='0', nullable=False)
    question_report_count = Column(Integer, server_default='0', nullable=False)
    question_reported_count = Column(Integer, server_default='0', nullable=False)
    question_upvote_count = Column(Integer, server_default='0', nullable=False)
    question_upvoted_count = Column(Integer, server_default='0', nullable=False)
    question_downvote_count = Column(Integer, server_default='0', nullable=False)
    question_downvoted_count = Column(Integer, server_default='0', nullable=False)

    answers = relationship("Answer", cascade='all,delete-orphan')
    @aggregated('answers', Column(Integer, server_default="0", nullable=False))
    def answer_aggregated_count(self):
        return func.coalesce(func.sum(
            func.if_(text('IFNULL(is_deleted, False) <> True') & text('IFNULL(is_anonymous, False) <> True'),1, 0)), 0)
    @property
    def answer_count(self):
        if self.answer_aggregated_count is None:
            self.answer_aggregated_count = 0

        if g.current_user and g.current_user.id == self.id:
            Answer = get_model('Answer')
            anonymous_count = Answer.query.with_entities(func.count(Answer.id)).filter( \
                (Answer.user_id == self.id) &
                (Answer.is_deleted != True) &
                (Answer.is_anonymous == True)).scalar()
            return self.answer_aggregated_count + anonymous_count
        return self.answer_aggregated_count
    answer_share_count = Column(Integer, server_default='0', nullable=False)
    answer_shared_count = Column(Integer, server_default='0', nullable=False)
    answer_upvote_count = Column(Integer, server_default='0', nullable=False)
    answer_upvoted_count = Column(Integer, server_default='0', nullable=False)
    answer_downvote_count = Column(Integer, server_default='0', nullable=False)
    answer_downvoted_count = Column(Integer, server_default='0', nullable=False)
    answer_report_count = Column(Integer, server_default='0', nullable=False)
    answer_reported_count = Column(Integer, server_default='0', nullable=False)

    articles = relationship("Article", cascade='all,delete-orphan')
    @aggregated('articles', Column(Integer, server_default="0", nullable=False))
    def article_aggregated_count(self):
        return func.coalesce(
            func.sum(func.if_(text('is_deleted <> 1') & text('is_anonymous <> 1'), 1, 0)), 0)
    @property
    def article_count(self):
        if self.article_aggregated_count is None:
            self.article_aggregated_count = 0

        if g.current_user and g.current_user.id == self.id:
            Article = get_model('Article')
            anonymous_count = Article.query.with_entities(func.count(Article.id)).filter( \
                (Article.user_id == self.id) &
                (Article.is_deleted != True) &
                (Article.is_anonymous == True)).scalar()
            return self.article_aggregated_count + anonymous_count
        return self.article_aggregated_count
    article_share_count = Column(Integer, server_default='0', nullable=False)
    article_shared_count = Column(Integer, server_default='0', nullable=False)
    article_upvote_count = Column(Integer, server_default='0', nullable=False)
    article_upvoted_count = Column(Integer, server_default='0', nullable=False)
    article_downvote_count = Column(Integer, server_default='0', nullable=False)
    article_downvoted_count = Column(Integer, server_default='0', nullable=False)
    article_report_count = Column(Integer, server_default='0', nullable=False)
    article_reported_count = Column(Integer, server_default='0', nullable=False)


    @aggregated('polls', Column(Integer, server_default="0", nullable=False))
    def poll_aggregated_count(self):
        return func.coalesce(
            func.sum(func.if_(text('is_anonymous <> 1'), 1, 0)), 0)
    @property
    def poll_count(self):
        if self.poll_aggregated_count is None:
            self.poll_aggregated_count = 0

        if g.current_user and g.current_user.id == self.id:
            Poll = get_model('Poll')
            anonymous_count = Poll.query.with_entities(func.count(Poll.id)).filter( \
                (Poll.user_id == self.id) &
                (Poll.is_anonymous == True)).scalar()
            return self.poll_aggregated_count + anonymous_count
        return self.poll_aggregated_count
    poll_share_count = Column(Integer, server_default='0', nullable=False)
    poll_shared_count = Column(Integer, server_default='0', nullable=False)
    poll_upvote_count = Column(Integer, server_default='0', nullable=False)
    poll_upvoted_count = Column(Integer, server_default='0', nullable=False)
    poll_downvote_count = Column(Integer, server_default='0', nullable=False)
    poll_downvoted_count = Column(Integer, server_default='0', nullable=False)
    poll_report_count = Column(Integer, server_default='0', nullable=False)
    poll_reported_count = Column(Integer, server_default='0', nullable=False)

    @aggregated('posts', Column(Integer, server_default="0", nullable=False))
    def post_aggregated_count(self):
        return func.coalesce(
            func.sum(func.if_(text('is_anonymous <> 1'), 1, 0)), 0)

    @property
    def post_count(self):
        if self.post_aggregated_count is None:
            self.post_aggregated_count = 0

        if g.current_user and g.current_user.id == self.id:
            Post = get_model('Post')
            anonymous_count = Post.query.with_entities(func.count(Post.id)).filter( \
                (Post.user_id == self.id) &
                (Post.is_anonymous == True)).scalar()
            return self.post_aggregated_count + anonymous_count
        return self.post_aggregated_count
    post_share_count = Column(Integer, server_default='0', nullable=False)
    post_shared_count = Column(Integer, server_default='0', nullable=False)
    post_favorite_count = Column(Integer, server_default='0', nullable=False)
    post_favorited_count = Column(Integer, server_default='0', nullable=False)
    post_report_count = Column(Integer, server_default='0', nullable=False)
    post_reported_count = Column(Integer, server_default='0', nullable=False)

    comment_count = Column(Integer, server_default='0', nullable=False)
    comment_favorite_count = Column(Integer, server_default='0', nullable=False)
    comment_favorited_count = Column(Integer, server_default='0', nullable=False)
    comment_report_count = Column(Integer, server_default='0', nullable=False)
    comment_reported_count = Column(Integer, server_default='0', nullable=False)

    topic_follow_count = Column(Integer, server_default='0', nullable=False)
    followed_topics = relationship('Topic', secondary='topic_follow', lazy='dynamic')
    @aggregated('followed_topics', Column(Integer, server_default="0", nullable=False))
    def topic_followed_count(self):
        return func.count('1')
    created_topics = relationship('Topic', lazy='dynamic')
    @aggregated('created_topics', Column(Integer, server_default="0", nullable=False))
    def topic_created_count(self):
        return func.count('1')

    user_report_count = Column(Integer, server_default='0', nullable=False)
    user_reported_count = Column(Integer, server_default='0', nullable=False)
    @property
    def user_follow_count(self):
        followers = UserFollow.query.with_entities(UserFollow.follower_id).filter(
            UserFollow.followed_id == self.id).all()
        follower_ids = [follower[0] for follower in followers]
        follower_count = User.query.with_entities(func.count(User.id)) \
            .filter(User.id.in_(follower_ids)) \
            .filter(text('IFNULL(is_deactivated, False) = False')) \
            .scalar()
        return follower_count
    @property
    def user_followed_count(self):
        followeds = UserFollow.query.with_entities(UserFollow.followed_id).filter(
            UserFollow.follower_id == self.id).all()
        followed_ids = [followed[0] for followed in followeds]
        followed_count = User.query.with_entities(func.count(User.id)) \
            .filter(User.id.in_(followed_ids)) \
            .filter(text('IFNULL(is_deactivated, False) = False')) \
            .scalar()
        return followed_count
    @property
    def friend_count(self):
        UserFriend = get_model('UserFriend')
        friend_count = UserFriend.query.with_entities(UserFriend.id).filter( \
            (UserFriend.friend_id == self.id) |
            (UserFriend.friended_id == self.id)).count()
        return friend_count
    @property
    def endorsed_count(self):
        try:
            TopicUserEndorse = get_model('TopicUserEndorse')
            if g.endorsed_topic_id:
                endorsed_count = TopicUserEndorse.query.with_entities(TopicUserEndorse.id).filter(
                    TopicUserEndorse.endorsed_id == self.id,
                    TopicUserEndorse.topic_id == g.endorsed_topic_id).count()
                return endorsed_count
            return 0
        except Exception as e:
            print(e)

    @aggregated('sent_friend_requests', Column(Integer))
    def friends_sent_count(self):
        return func.count('1')

    @aggregated('received_friend_requests', Column(Integer))
    def friend_received_count(self):
        return func.count('1')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user

    def get_user_by_phone_number(phone_number):
        user = User.query.filter_by(phone_number=phone_number).first()
        return user

    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user

    @property
    def is_online(self):
        return abs(self.last_seen - datetime.now()).total_seconds() < 60

    @property
    def is_super_admin(self):
        return UserRole.is_super_admin(self.admin)


    @property
    def is_endorsed_by_me(self):
        TopicUserEndorse = get_model('TopicUserEndorse')
        if g.current_user:
            if g.endorsed_topic_id:
                endorsed = TopicUserEndorse.query.with_entities(TopicUserEndorse.id).filter(
                    TopicUserEndorse.user_id == g.current_user.id,
                    TopicUserEndorse.endorsed_id == self.id,
                    TopicUserEndorse.topic_id == g.endorsed_topic_id).first()
                return True if endorsed else False
            return False
        return False

    @property
    def is_approved_friend(self):
        UserFriend = get_model('UserFriend')
        if g.current_user:
            friend = UserFriend.query.with_entities(UserFriend.id).filter( \
                ((UserFriend.friended_id == g.current_user.id) & (UserFriend.friend_id == self.id)) |
                ((UserFriend.friend_id == g.current_user.id) & (UserFriend.friended_id == self.id))
            ).first()
            return True if friend else False
        return False

    @property
    def is_friend_requested(self):
        UserFriend = get_model('UserFriend')
        if g.current_user:
            friend = UserFriend.query.with_entities(UserFriend.id).filter(UserFriend.friend_id == self.id,
                                                                          UserFriend.friended_id == g.current_user.id).first()
            return True if friend else False
        return False

    @property
    def is_friended_by_me(self):
        UserFriend = get_model('UserFriend')
        if g.current_user:
            friend = UserFriend.query.with_entities(UserFriend.id).filter(UserFriend.friend_id == g.current_user.id,
                                                                          UserFriend.friended_id == self.id).first()
            return True if friend else False
        return False

    @property
    def is_followed_by_me(self):
        UserFollow = get_model('UserFollow')
        if g.current_user:
            follow = UserFollow.query.with_entities(UserFollow.id).filter(UserFollow.follower_id == g.current_user.id,
                                                                          UserFollow.followed_id == self.id).first()
            return True if follow else False
        return False

    @property
    def is_facebook_linked(self):
        SocialAccount = get_model('SocialAccount')
        social_account = SocialAccount.query.with_entities(SocialAccount.id).filter(
            (SocialAccount.user_id == self.id) & (SocialAccount.provider == 'facebook')
        ).first()
        return True if social_account else False

    @property
    def is_google_linked(self):
        SocialAccount = get_model('SocialAccount')
        social_account = SocialAccount.query.with_entities(SocialAccount.id).filter(
            (SocialAccount.user_id == self.id) & (SocialAccount.provider == 'google')
        ).first()
        return True if social_account else False


class UserLocation(Model):
    __tablename__ = 'user_location'

    id = Column(Integer, primary_key=True)
    location_detail = Column(UnicodeText)
    start_year = Column(Integer)
    end_year = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', lazy=True) 
    updated_date = Column(DateTime, default=datetime.utcnow)
    created_date = Column(DateTime, default=datetime.utcnow)
    is_current = Column(Boolean, server_default=expression.false())
    is_visible = Column(Boolean, server_default=expression.false())


class UserLanguage(Model):
    __tablename__ = 'user_language'

    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey('language.id', ondelete='CASCADE'), nullable=False, index=True)
    language = relationship('Language', lazy=True)  
    level = Column(UnicodeText)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', lazy=True)  
    updated_date = Column(DateTime, default=datetime.utcnow)
    created_date = Column(DateTime, default=datetime.utcnow)
    is_visible = Column(Boolean, server_default=expression.false())


class UserEducation(Model):
    __tablename__ = 'user_education'

    id = Column(Integer, primary_key=True)
    school = Column(UnicodeText)
    primary_major = Column(UnicodeText)
    secondary_major = Column(UnicodeText)
    start_year = Column(Integer)
    end_year = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', lazy=True)
    updated_date = Column(DateTime, default=datetime.utcnow)
    created_date = Column(DateTime, default=datetime.utcnow)
    is_current = Column(Boolean, server_default=expression.false())
    is_visible = Column(Boolean, server_default=expression.false())


class UserEmployment(Model):
    __tablename__ = 'user_employment'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    position = Column(String(255))
    company = Column(String(255))
    start_year = Column(Integer)
    end_year = Column(Integer)
    created_date = Column(DateTime, default=datetime.utcnow)
    is_current = Column(Boolean, server_default=expression.false())
    is_visible = Column(Boolean, server_default=expression.false())


class UserPermission(Model):
    __tablename__ = 'user_permission'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), index=True)
    permission_id = Column(ForeignKey('permission.id', ondelete='CASCADE'), index=True)
    allow = Column(Boolean, server_default=expression.false())


class UserTopic(Model):
    __tablename__ = 'user_topic'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id', ondelete='CASCADE'), nullable=False, index=True)
    topic = relationship('Topic', foreign_keys=[topic_id], lazy=True)
    description = Column(UnicodeText)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', lazy=True)
    updated_date = Column(DateTime, default=datetime.utcnow)
    created_date = Column(DateTime, default=datetime.utcnow)
    is_visible = Column(Boolean, server_default=expression.false())


class UserSeenQuestion(Model):
    """Define the questions that the user has seen."""
    __tablename__ = 'user_seen_question'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', backref=backref("seen_question_users", cascade="all, delete-orphan"), lazy=True) 
    question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'), nullable=True, index=True)
    question = relationship('Question', backref=backref("seen_items", cascade="all, delete-orphan"), lazy=True)
    created_date = Column(DateTime, default=datetime.utcnow)


class UserSeenPost(Model):
    """
    Define the posts that the user has seen.
    """
    __tablename__ = 'user_seen_post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', backref=backref("seen_post_users", cascade="all, delete-orphan"), lazy=True)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='CASCADE'), nullable=True, index=True)
    post = relationship('Post', backref=backref("seen_items", cascade="all, delete-orphan"), lazy=True)
    created_date = Column(DateTime, default=datetime.utcnow)


class UserSeenArticle(Model):
    """
    Define the articles that the user has seen.
    """
    __tablename__ = 'user_seen_article'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', backref=backref("seen_article_users", cascade="all, delete-orphan"), lazy=True) 
    article_id = Column(Integer, ForeignKey('article.id', ondelete='CASCADE'), nullable=True, index=True)
    article = relationship('Article', backref=backref("seen_items", cascade="all, delete-orphan"), lazy=True)
    created_date = Column(DateTime, default=datetime.utcnow)


class UserSeenPoll(Model):
    """
    Define the poll that the user has seen.
    """
    __tablename__ = 'user_seen_poll'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', backref=backref("seen_poll_users", cascade="all, delete-orphan"), lazy=True)
    poll_id = Column(Integer, ForeignKey('poll.id', ondelete='CASCADE'), nullable=True, index=True)
    poll = relationship('Poll', backref=backref("seen_items", cascade="all, delete-orphan"), lazy=True)
    created_date = Column(DateTime, default=datetime.utcnow)


class UserMailedQuestion(Model):
    """
    Define the questions that the user has been mailed.
    Used to keep track of recommendation mailing tasks.
    """
    __tablename__ = 'user_mailed_question'

    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', backref=backref("mailed_question_users", cascade="all, delete-orphan"), lazy=True)  # one-to-many relationship with table Post
    question_id = Column(Integer, ForeignKey('question.id', ondelete='CASCADE'), nullable=True, index=True)
    question = relationship('Question', backref=backref("mailed_items", cascade="all, delete-orphan"), lazy=True)  # one-to-many relationship with table Post
    created_date = Column(DateTime, default=datetime.utcnow)


class UserMailedArticle(Model):
    """
    Define the articles that the user has been mailed.
    Used to keep track of recommendation mailing tasks.
    """
    __tablename__ = 'user_mailed_article'

    def __init__(self, user_id, article_id):
        self.user_id = user_id
        self.article_id = article_id

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = relationship('User', backref=backref("mailed_article_users", cascade="all, delete-orphan"), lazy=True)  # one-to-many relationship with table Post
    article_id = Column(Integer, ForeignKey('article.id', ondelete='CASCADE'), nullable=True, index=True)
    article = relationship('Article', backref=backref("mailed_items", cascade="all, delete-orphan"), lazy=True)  # one-to-many relationship with table Post
    created_date = Column(DateTime, default=datetime.utcnow)

