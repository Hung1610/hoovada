#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail

# own modules
from app.settings.config import config_by_name

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail = Mail()


def init_app(config_name):
    app = Flask(__name__)
    CORS(app)
    # app.config['RESTFUL_JSON'] = {
    #     'ensure_ascii': False,
    #     'encoding':'utf8'
    # }
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    return app
