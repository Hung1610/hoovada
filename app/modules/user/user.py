#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import aggregated

# own modules
from app.modules.common.model import Model
from app import db

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class SignupUser(Model):
    """
    Define the SignUpUser Model.
    """
    __tablename__ = 'signup_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    registered_date = db.Column(db.Date)
    registered_time = db.Column(db.Time)
    activation_code = db.Column(db.String(255))
    code_created_date = db.Column(db.Date)
    code_created_time = db.Column(db.Time)
    code_duration_time = db.Column(db.Float)
    code_sent_date = db.Column(db.Date)
    code_sent_time = db.Column(db.Time)
    trial_number = db.Column(db.Integer)
    confirm = db.Column(db.Boolean)


class RecoveryUser(Model):
    """
    Define the RecoveryUser model.
    """
    __tablename__ = 'recovery_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    new_password_hash = db.Column(db.String(255))
    required_date = db.Column(db.Date)
    required_time = db.Column(db.Time)
    recovery_code = db.Column(db.String(255))
    code_created_date = db.Column(db.Date)
    code_created_time = db.Column(db.Time)
    code_duration_time = db.Column(db.Float)
    code_sent_date = db.Column(db.Date)
    code_sent_time = db.Column(db.Time)
    trial_number = db.Column(db.Integer)
    continued = db.Column(db.Boolean)
    session_start_date = db.Column(db.Date)
    session_start_time = db.Column(db.Time)
    session_duration = db.Column(db.Float)
    recovered = db.Column(db.Boolean)


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
    profile_pic_data_url = db.Column(db.String(255))  # (10000), default='')
    admin = db.Column(db.Boolean, default=False)
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
    # hoovada_digests_frequency_setting = db.Column(db.String(255)(6), nullable=False, default='weekly')
    hoovada_digests_frequency_setting = db.Column(db.String(255), default='weekly')

    questions_you_asked_or_followed_setting = db.Column(db.Boolean, default=True)
    # questions_you_asked_or_followed_frequency_setting = db.Column(db.String(255)(6), nullable=False, default='weekly')
    questions_you_asked_or_followed_frequency_setting = db.Column(db.String(255), default='weekly')
    people_you_follow_setting = db.Column(db.Boolean, default=True)

    # people_you_follow_frequency_setting = db.Column(db.String(255)(6), nullable=False, default='weekly')
    people_you_follow_frequency_setting = db.Column(db.String(255), default='weekly')
    email_stories_topics_setting = db.Column(db.Boolean, default=True)
    # email_stories_topics_frequency_setting = db.Column(db.String(255)(6), nullable=False, default='weekly')
    email_stories_topics_frequency_setting = db.Column(db.String(255), default='weekly')
    last_message_read_time = db.Column(db.DateTime, default=datetime.utcnow)

    # count values used for statistics
    # question_count = db.Column(db.Integer, server_default='0')  # number of questions user created
    @aggregated('questions', db.Column(db.Integer))
    def question_count(self):
        return db.func.count('1')
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

    # answer_count = db.Column(db.Integer, server_default='0')  # number answers user created
    @aggregated('answers', db.Column(db.Integer))
    def answer_count(self):
        return db.func.count('1')
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

    topic_follow_count = db.Column(db.Integer, server_default='0')
    topic_followed_count = db.Column(db.Integer, server_default='0')
    topic_created_count = db.Column(db.Integer, server_default='0')

    user_follow_count = db.Column(db.Integer, server_default='0')
    user_followed_count = db.Column(db.Integer, server_default='0')

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

    # @hybrid_property
    # def about_me(self):
    #     """Return the value of _about_me but the html version."""
    #     return self._about_me_html
    #
    # @about_me.setter
    # def about_me(self, markdown):
    #     """Constrain markdown with html so html is never set directly"""
    #     # self._about_me = remove_markdown(markdown)
    #     # self._about_me_markdown = markdown
    #     # self._about_me_html = convert_markdown(markdown)
    #     pass

    # @hybrid_property
    # def about_me_markdown(self):
    #     """Return the value of _markdown."""
    #     return self.about_me_markdown
    #
    # @hybrid_property
    # def about_me_html(self):
    #     """Return the value of _html."""
    #     return self.about_me_html

    # @hybrid_property
    # def topics(self):
    #     """Return the value of _topics."""
    #     return self.topics
    #
    # @property
    # def current_user_topics(self):
    #     return self.topics + self.assigned_topics

    # def get_topicstring(self):
    #     """Return the topics for this instance as a comma separated string"""
    #     return ', '.join([topic.name for topic in self.topics])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # @property
    # def avatar(self):
    #     if self.profile_pic_url:
    #         return self.profile_pic_url
    #     if self.profile_pic_data_url:
    #         return self.profile_pic_data_url
    #     else:
    #         return url_for('static', filename='img/pro-pic.png', _scheme='https', _external=True)

    @property
    def is_admin(self):
        if self.admin:
            return True
        else:
            return False

    # @property
    # def is_authenticated(self):
    #     return True

    # @property
    # def is_active(self):
    #     return self.active # True

    # @property
    # def is_anonymous(self):
    #     return False

    # def get_id(self):
    #     try:
    #         return str(self.id)
    #     except AttributeError:
    #         raise NotImplementedError('No `id` attribute - override `get_id`')

    # @property
    # def name(self):
    #     if self.first_name and self.last_name:
    #         return f'{self.first_name} {self.last_name}'
    #     else:
    #         return f'{self.display_name}'

    # @property
    # def email_confirmed(self):
    #     if self.confirmed:
    #         return True
    #     else:
    #         return False

    # @validates('email')
    # def validate_email(self, key, address):
    #     assert '@' in address
    #     return address

    # class Meta:
    #     order_by = ('-joined_date')
    #
    # def __repr__(self):
    #     return (
    #         f'User [ID: {self.id}]\nName: {self.display_name}\nEmail: {self.email}'
    #     )
