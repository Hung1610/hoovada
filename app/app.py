#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache

# own modules
from app.settings.config import config_by_name

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."



def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)
SQLAlchemy.get_model = get_model

def get_model_by_tablename(self, tablename):
    for c in self.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c
SQLAlchemy.get_model_by_tablename = get_model_by_tablename

db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
mail = Mail()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def init_app(config_name):
    app = Flask(__name__,static_folder='static')
    CORS(app)
    # app.config['RESTFUL_JSON'] = {
    #     'ensure_ascii': False,
    #     'encoding':'utf8'
    # }
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config_by_name[config_name])
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    return app
