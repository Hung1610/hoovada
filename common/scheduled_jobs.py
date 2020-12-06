#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
from common.dramatiq_producers import send_recommendation_mail, send_similar_mail
from datetime import datetime, timedelta
from pytz import utc

# third-party modules
from flask import render_template
from flask_apscheduler import APScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# own modules
from common.models.model import db
from common.enum import FrequencySettingEnum
from common.utils.util import send_email

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


scheduler = APScheduler()


@scheduler.task('cron', id='send_registered_user_emails_job', day='*')
def send_registered_user_emails_job():
    """ Send email notification to admin. Contains list of newly registered users

    Returns:
        None
    """
    with scheduler.app.app_context():
        User = db.get_model('User')

        today_minus_one_week = datetime.now() - timedelta(weeks=1)
        users = User.query.filter(User.joined_date > today_minus_one_week).all()

        html = render_template('admin_registered_users_notification.html', users=users)
        for admin_email in scheduler.app.config['MAIL_ADMINS']:
            send_email(admin_email, 'User Registered On Hoovada', html)


@scheduler.task('cron', id='send_daily_recommendation_emails_job', minute='0', hour='0')
def send_daily_recommendation_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    with scheduler.app.app_context():
        User = db.get_model('User')

        users = User.query\
            .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

        for user in users:
            send_recommendation_mail.send(user)


@scheduler.task('cron', id='send_weekly_recommendation_emails_job', week='*', day_of_week='sun')
def send_weekly_recommendation_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    with scheduler.app.app_context():
        User = db.get_model('User')

        users = User.query\
            .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

        for user in users:
            send_recommendation_mail.send(user)


@scheduler.task('cron', id='send_daily_similar', minute='0', hour='0')
def send_daily_similar():
    """ Send daily emails to users. Contain similar articles/questions.

    Returns:
        None
    """
    with scheduler.app.app_context():
        User = db.get_model('User')

        users = User.query\
            .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

        for user in users:
            send_similar_mail.send(user)


@scheduler.task('cron', id='send_weekly_similar', week='*', day_of_week='sun')
def send_weekly_similar():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    with scheduler.app.app_context():
        User = db.get_model('User')

        users = User.query\
            .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

        for user in users:
            send_similar_mail.send(user)