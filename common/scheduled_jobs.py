#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
from datetime import datetime, timedelta
from pytz import utc

# third-party modules
from flask import current_app, render_template
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# own modules
from common.enum import FrequencySettingEnum
from common.utils.util import send_email

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

def send_registered_user_emails_job():
    """ Send email notification to admin. Contains list of newly registered users

    Returns:
        None
    """
    db = current_app.db_context
    User = db.get_model('User')

    today_minus_one_week = datetime.now() - timedelta(weeks=1)
    users = User.query.filter(User.joined_date > today_minus_one_week).all()

    html = render_template('admin_registered_users_notification.html', users=users)
    for admin_email in current_app.config['MAIL_ADMINS']:
        send_email(admin_email, 'User Registered On Hoovada', html)

def send_daily_recommendation_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    db = current_app.db_context
    User = db.get_model('User')
    Topic = db.get_model('Topic')
    TopicFollow = db.get_model('TopicFollow')
    Question = db.get_model('Question')
    Article = db.get_model('Article')

    users = User.query\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.daily.name)

    for user in users:
        if user.email:
            followed_topic_ids = TopicFollow.query.with_entities(TopicFollow.topic_id).filter(TopicFollow.user_id == user.id).all()
            recommended_questions = Question.query.filter(Question.topics.any(Topic.id.in_(followed_topic_ids)))
            recommended_articles = Article.query.filter(Article.topics.any(Topic.id.in_(followed_topic_ids)))
            html = render_template('recommendation_for_user.html', \
                user=user, recommended_articles=recommended_articles, recommended_question=recommended_questions)
            send_email(user.email, 'Recommended Questions and Articles On Hoovada', html)

def send_weekly_recommendation_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    db = current_app.db_context
    User = db.get_model('User')
    Topic = db.get_model('Topic')
    TopicFollow = db.get_model('TopicFollow')
    Question = db.get_model('Question')
    Article = db.get_model('Article')

    users = User.query\
        .filter(User.hoovada_digests_setting == True, User.hoovada_digests_frequency_setting == FrequencySettingEnum.weekly.name)

    for user in users:
        if user.email:
            followed_topic_ids = TopicFollow.query.with_entities(TopicFollow.topic_id).filter(TopicFollow.user_id == user.id).all()
            recommended_questions = Question.query.filter(Question.topics.any(Topic.id.in_(followed_topic_ids)))
            recommended_articles = Article.query.filter(Article.topics.any(Topic.id.in_(followed_topic_ids)))
            html = render_template('recommendation_for_user.html', \
                user=user, recommended_articles=recommended_articles, recommended_question=recommended_questions)
            send_email(user.email, 'Recommended Questions and Articles On Hoovada', html)

def get_scheduler(app):
    # ApScheduler
    scheduler = BackgroundScheduler()
    jobstores = {
        'default': RedisJobStore(\
            db=1,\
            port=app.config['REDIS_PORT'],\
            host=app.config['REDIS_HOST'],\
            password=app.config['REDIS_PASSWORD']\
        )
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler.configure(\
        jobstores=jobstores,\
        executors=executors,\
        job_defaults=job_defaults,\
        timezone=utc)
    scheduler.add_job(send_registered_user_emails_job, trigger='interval', days=7)
    scheduler.add_job(send_daily_recommendation_emails_job, trigger='interval', days=1)
    scheduler.add_job(send_weekly_recommendation_emails_job, trigger='interval', days=7)
    return scheduler
