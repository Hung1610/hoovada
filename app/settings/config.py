#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ, path, pardir

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

    # Cache configuration   # Flask-Caching related configs
    # Simple cache using Python dictionary
    # CACHE_TYPE = "simple"
    # Redis cache using redis database
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'fcache'
    CACHE_REDIS_HOST = '139.59.248.38'
    CACHE_REDIS_PORT = '31930'
    CACHE_REDIS_URL = 'redis://139.59.248.38:31930'
    CACHE_REDIS_PASSWORD = '74HPHt3ewf'

    CACHE_DEFAULT_TIMEOUT = 300

    # Email configuration
    MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = False
    MAIL_USERNAME =  environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com') 
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD', 'xrkajeadxbexdell')
    ADMINS = ['admin@hoovada.com'] # list of emails to receive error reports

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
    BCRYPT_LOG_ROUNDS = 13 # Number of times a password is hashed
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # social
    FACEBOOK_SECRET = environ.get('FACEBOOK_SECRET', '') 
    GRAPH_API_URL = 'https://graph.facebook.com/me?'
    FACEBOOK_FIELDS = [
        'id',
        'name',
        'address',
        'birthday',
        'email',
        'first_name',
        'gender',
        'last_name',
        'middle_name',
        'photos',
        'picture'
    ]
    GOOGLE_PROFILE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
    
    # Twilio API credentials
    # (find here https://www.twilio.com/console)
    TWILIO_ACCOUNT_SID = environ.get('YOUR_TWILIO_ACCOUNT_SID', 'AC3bc87a9ca0dc5bcc55c263b00bd583c1')
    TWILIO_AUTH_TOKEN = environ.get('YOUR_TWILIO_AUTH_TOKEN', 'b2e699d59ef37fb757260178cdf1e3bb') # TEST Credentials
    # (create one here https://www.twilio.com/console/verify/services)
    VERIFICATION_SID = environ.get('YOUR_VERIFICATION_SID', 'VAc2d0ecc3630b615db53742c8ef825fbd')
    LIMIT_VERIFY_SMS_TIME = 60 # 60seconds


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
