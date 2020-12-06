#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime
from logging.config import dictConfig

# third-party modules
from flask import Flask, g, request
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

# own modules
from app.settings import config_by_name
from app.dramatiq_consumers import dramatiq
from common.models.model import db
from common.scheduled_jobs import scheduler
from common.utils.util import (get_logged_user, get_model,
                               get_model_by_tablename)

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


# Flask plugins
migrate = Migrate()
flask_bcrypt = Bcrypt()
mail = Mail()
cache = Cache()

# Flask app utility functions
Flask.db_context = db
Flask.mail_context = mail
Flask.cache_context = cache
Flask.get_logged_user = get_logged_user
app = Flask(__name__, static_folder='static')

# Prometheus metrics exporter
metrics = GunicornInternalPrometheusMetrics(app)
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

def init_app():
    # Setup Flask app
    app.config.from_object(config_by_name[app.config['ENV']])
    @app.before_request
    def before_request():
        g.current_user, _ = app.get_logged_user(request)
        g.current_user_is_admin = False
        if g.current_user:
            g.current_user.last_seen = datetime.now()
            db.session.commit()
    # Config CORS
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
    # Config dramatiq
    dramatiq.init_app(app)
    # Config ApScheduler
    scheduler.init_app(app)
    scheduler.start()
    return app
