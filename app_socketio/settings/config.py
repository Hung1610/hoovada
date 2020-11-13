#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class BaseConfig:
    # debug mode is turned off by default
    DEBUG = False

    # flask configuration
    SECRET_KEY = environ.get('SECRET_KEY', 'f495b66803a6512d')
    SECURITY_SALT = environ.get('SECURITY_SALT', '14be1971fc014f1b84')

    # Email configuration
    MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = False
    MAIL_USERNAME =  environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com') 
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD', 'xrkajeadxbexdell')
    MAIL_ADMINS = ['admin@hoovada.com'] # list of emails to receive error reports

    # need to set this so that email can be sent
    MAIL_SUPPRESS_SEND = False
    TESTING = False

    # Wasabi service
    S3_BUCKET = environ.get('S3_BUCKET', 'hoovada') # test bucket
    WASABI_ACCESS_KEY = environ.get('WASABI_ACCESS_KEY', '') # test bucket
    WASABI_SECRET_ACCESS_KEY = environ.get('WASABI_SECRET_ACCESS_KEY', '')  

    # mysql configuration
    DB_USER = environ.get('DB_USER', 'dev')
    DB_PASSWORD = environ.get('DB_PASSWORD', 'hoovada')
    DB_HOST = environ.get('DB_HOST', 'localhost')
    DB_PORT = environ.get('DB_PORT', '3306') 
    DB_NAME = environ.get('DB_NAME', 'hoovada')
    DB_CHARSET = 'utf8mb4'

    # other configurations
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_ECHO = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    SWAGGER_UI_DOC_EXPANSION = 'none'
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True

    # if you want to use mysql 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
         user=BaseConfig.DB_USER,
         password=BaseConfig.DB_PASSWORD,
         host=BaseConfig.DB_HOST,
         port=BaseConfig.DB_PORT,
         name=BaseConfig.DB_NAME,
         charset=BaseConfig.DB_CHARSET
     )


class ProductionConfig(BaseConfig):
    """production configuration."""
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
         user=BaseConfig.DB_USER,
         password=BaseConfig.DB_PASSWORD,
         host=BaseConfig.DB_HOST,
         port=BaseConfig.DB_PORT,
         name=BaseConfig.DB_NAME,
         charset=BaseConfig.DB_CHARSET
     )


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = BaseConfig.SECRET_KEY
