#!/usr/bin/python
# -*- coding: utf-8 -*-

# bulit-in modules
from os import environ
import sys
import datetime
import time
import signal

# third-party modules
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

# own modules
from common.dramatiq_producers import send_daily_new_topics, send_daily_recommendation_mails, send_daily_similar_mails, send_weekly_new_topics, send_weekly_recommendation_mails, send_weekly_registered_users, send_weekly_similar_mails

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

# redis configuration
REDIS_PORT = environ.get('REDIS_PORT', '6380')
REDIS_HOST = environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PASSWORD = environ.get('REDIS_PASSWORD', 'hoovada')

# mysql configuration
DB_USER = environ.get('DB_USER', 'dev')
DB_PASSWORD = environ.get('DB_PASSWORD', 'hoovada')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_PORT = environ.get('DB_PORT', '3306')
DB_NAME = environ.get('DB_NAME', 'hoovada')
DB_CHARSET = 'utf8mb4'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
        charset=DB_CHARSET
    )

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

def send_daily_new_topics_job():
    """ Send daily emails to users. Contain new topics.

    Returns:
        None
    """
    send_daily_new_topics.send()

def send_weekly_new_topics_job():
    """ Send weekly emails to users. Contain new topics.

    Returns:
        None
    """
    send_weekly_new_topics.send()

def health_check():
    print('BACKGROUND JOB WORKING ', datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)

def get_scheduler():
    # ApScheduler
    scheduler = BackgroundScheduler()

    sqlalchemy_job_store = SQLAlchemyJobStore(SQLALCHEMY_DATABASE_URI)
    
    # redis_job_store = RedisJobStore(db=1,\
    #         host=REDIS_HOST,\
    #         port=REDIS_PORT,\
    #         password=REDIS_PASSWORD)

    jobstores = {
        'default': sqlalchemy_job_store,
        # 'redis': redis_job_store,
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
    scheduler.add_job(health_check, 'interval', minutes=1, id='health_check', replace_existing=True)
    scheduler.add_job(send_registered_user_emails_job, 'cron', day_of_week='sun', week='*', hour=0, minute=0, id='send_registered_user_emails_job', replace_existing=True)
    scheduler.add_job(send_daily_recommendation_emails_job, 'cron', minute=0, hour=0, id='send_daily_recommendation_emails_job', replace_existing=True)
    scheduler.add_job(send_weekly_recommendation_emails_job, 'cron', day_of_week='sun', week='*', hour=0, minute=0, id='send_weekly_recommendation_emails_job', replace_existing=True)
    scheduler.add_job(send_daily_similar_emails_job, 'cron', minute=0, hour=0, id='send_daily_similar_emails_job', replace_existing=True)
    scheduler.add_job(send_weekly_similar_emails_job, 'cron', day_of_week='sun', week='*', hour=0, minute=0, id='send_weekly_similar_emails_job', replace_existing=True)
    
    return scheduler

def gracefully_shutdown_scheduler(scheduler):
    try:
        print('Shutting down job scheduler', flush=True)
        scheduler.shutdown(wait=False)
    except Exception as e: 
        print(e, flush=True)
        pass
    sys.exit(0)

if __name__ == "__main__":
    apscheduler = get_scheduler()
    signal.signal(signal.SIGTERM, lambda num, frame: gracefully_shutdown_scheduler(apscheduler))
    apscheduler.print_jobs()
    apscheduler.start()
    while True:
        time.sleep(1)
