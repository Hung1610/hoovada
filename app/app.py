#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from pytz import utc

# third-party modules
from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# own modules
from app.settings.config import config_by_name
from common.utils.util import get_model, get_model_by_tablename, get_logged_user
from common.scheduled_jobs import add_jobs

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


SQLAlchemy.get_model = get_model
SQLAlchemy.get_model_by_tablename = get_model_by_tablename
db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
mail = Mail()
cache = Cache()

Flask.db_context = db
Flask.mail_context = mail
Flask.cache_context = cache
Flask.get_logged_user = get_logged_user
app = Flask(__name__, static_folder='static')

scheduler = BackgroundScheduler()

@app.before_request
def before_request():
    g.current_user, _ = app.get_logged_user(request)
    g.current_user_is_admin = False

def init_app(config_name):
    # Setup Flask app
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config_by_name[config_name])
    CORS(app)
    # Config Flask-Cache
    cache.init_app(app)
    # Config Flask-SqlAlchemy
    db.init_app(app)
    # Config Flask-Migrate
    migrate.init_app(app, db)
    # Config Flask-Bycrypt
    flask_bcrypt.init_app(app)
    # Config Flask-Mail
    mail.init_app(app)
    # Config ApScheduler
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
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
    add_jobs(scheduler)
    return app
