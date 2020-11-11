#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from logging.config import dictConfig
from pytz import utc

# third-party modules
from flask import Flask, g, request
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

# own modules
from app.settings.config import config_by_name
from common.scheduled_jobs import add_jobs
from common.utils.util import (get_logged_user, get_model,
                               get_model_by_tablename)

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


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
metrics = GunicornInternalPrometheusMetrics(app)
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

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
    # scheduler.start()
    return app
