#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bulit-in modules
from os import environ

# third-party modules
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# own modules
from common.dramatiq_producers import send_daily_recommendation_mails, send_daily_similar_mails, send_weekly_recommendation_mails, send_weekly_registered_users, send_weekly_similar_mails

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

REDIS_PORT = environ.get('REDIS_PORT', '6380')
REDIS_HOST = environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PASSWORD = environ.get('REDIS_PASSWORD', 'hoovada')

def send_registered_user_emails_job():
    """ Send email notification to admin. Contains list of newly registered users

    Returns:
        None
    """
    send_weekly_registered_users.send()

def send_daily_recommendation_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    send_daily_recommendation_mails.send()

def send_weekly_recommendation_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    send_weekly_recommendation_mails.send()

def send_daily_similar_emails_job():
    """ Send daily emails to users. Contain similar articles/questions.

    Returns:
        None
    """
    send_daily_similar_mails.send()

def send_weekly_similar_emails_job():
    """ Send daily emails to users. Contain recommendations.

    Returns:
        None
    """
    send_weekly_similar_mails.send()

def health_check():
    print('BACKGROUND JOB WORKING')

def get_scheduler():
    # ApScheduler
    scheduler = BlockingScheduler()
    
    redis_job_store = RedisJobStore(db=1,\
            host=REDIS_HOST,\
            port=REDIS_PORT,\
            password=REDIS_PASSWORD)
    jobstores = {
        'default': redis_job_store
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
        timezone=environ.get('TZ','Asia/Ho_Chi_Minh'))
    scheduler.add_job(health_check, 'interval', seconds=5)
    scheduler.add_job(send_registered_user_emails_job, 'cron', day_of_week='sun', week='*', hour=0, minute=0)
    scheduler.add_job(send_daily_recommendation_emails_job, 'cron', minute=0, hour=0)
    scheduler.add_job(send_weekly_recommendation_emails_job, 'cron', day_of_week='sun', week='*', hour=0, minute=0)
    scheduler.add_job(send_daily_similar_emails_job, 'cron', minute=0, hour=0)
    scheduler.add_job(send_weekly_similar_emails_job, 'cron', day_of_week='sun', week='*', hour=0, minute=0)
    return scheduler

if __name__ == "__main__":
    apscheduler = get_scheduler()
    apscheduler.start()