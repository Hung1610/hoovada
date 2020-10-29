#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache

# own modules
from app.settings.config import config_by_name
from common.utils.util import get_model, get_model_by_tablename, get_logged_user

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

@app.before_request
def before_request():
    g.current_user, _ = app.get_logged_user(request)
    g.current_user_is_admin = False

def init_app(config_name):
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config_by_name[config_name])
    CORS(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    return app
