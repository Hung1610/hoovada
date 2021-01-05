#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from logging.config import dictConfig

# third-party modules
from flask import Flask, g, request
from flask_cors import CORS
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from sqlalchemy_utils import create_database, database_exists

# own modules
from app.settings import config_by_name

# Flask plugins
from common.models import *
from common.utils.util import get_logged_user
from common.bcrypt import bcrypt
from common.cache import cache
from common.mail import mail
from common.db import db, migrate

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

# Config logging output
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

def init_basic_app():
    # Flask initilization
    Flask.get_logged_user = get_logged_user
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_by_name[app.config['ENV']])
    # Setup Flask app
    @app.before_request
    def before_request():
        g.current_user, _ = app.get_logged_user(request)
        g.current_user_is_admin = False
        g.endorsed_topic_id = None
        g.negative_rep_points = -2
        if g.current_user:
            g.current_user.last_seen = datetime.now()
            db.session.commit()
    return app


# Prometheus metrics exporter
metrics = GunicornInternalPrometheusMetrics(init_basic_app())
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

def init_app():
    app = init_basic_app()
    # Config CORS
    CORS(app)
    # Config Flask-Cache
    cache.init_app(app)
    # Config Flask-SqlAlchemy
    url = app.config['SQLALCHEMY_DATABASE_URI']
    if not database_exists(url):
        create_database(url)
    db.init_app(app)
    # Config Flask-Migrate
    migrate.init_app(app, db)
    # Config Flask-Bycrypt
    bcrypt.init_app(app)
    # Config Flask-Mail
    mail.init_app(app)
    return app
