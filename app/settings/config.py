#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import os

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class BaseConfig:
    # debug mode is turned off by default
    DEBUG = False

    # flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'f495b66803a6512d')
    SECURITY_SALT = os.environ.get('SECURITY_SALT', '14be1971fc014f1b84')

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = False
    MAIL_USERNAME =  os.environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'xrkajeadxbexdell')
    MAIL_SUPPRESS_SEND = False
    ADMINS = ['admin@hoovada.com'] # list of emails to receive error reports

    # need to set this so that email can be sent
    MAIL_SUPPRESS_SEND = False
    TESTING = False

    # Wasabi service
    WASABI_ACCESS_KEY = os.environ.get('WASABI_ACCESS_KEY', '') # test bucket
    WASABI_SECRET_ACCESS_KEY = os.environ.get('WASABI_SECRET_ACCESS_KEY', '')  

    # mysql configuration
    DB_USER = os.environ.get('DB_USER', 'dev')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'hoovada')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306') 
    DB_NAME = os.environ.get('DB_NAME', 'hoovada')
    DB_CHARSET = 'utf8mb4'

    # Locations
    APP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    IMAGE_FOLDER = '/images'
    AVATAR_FOLDER = os.path.join(IMAGE_FOLDER, 'avatars')

    # other configurations
    BCRYPT_LOG_ROUNDS = 13 # Number of times a password is hashed
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # social
    FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET', '') 
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
    TWILIO_ACCOUNT_SID = os.environ.get('YOUR_TWILIO_ACCOUNT_SID', 'AC3bc87a9ca0dc5bcc55c263b00bd583c1')
    TWILIO_AUTH_TOKEN = os.environ.get('YOUR_TWILIO_AUTH_TOKEN', 'b2e699d59ef37fb757260178cdf1e3bb') # TEST Credentials
    # (create one here https://www.twilio.com/console/verify/services)
    VERIFICATION_SID = os.environ.get('YOUR_VERIFICATION_SID', 'VAc2d0ecc3630b615db53742c8ef825fbd')
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
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get", "post"]


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
