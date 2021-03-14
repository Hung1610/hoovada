#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CommonBaseConfig:
    # debug mode is turned off by default
    DEBUG = False

    WEB_PROTOCOL = environ.get('WEB_PROTOCOL', 'https')

    DOMAIN_URL = WEB_PROTOCOL + '://' + environ.get('DOMAIN_ENDPOINT', 'localhost:5000')

    JSON_AS_ASCII = False

    # The name of the model used as User class
    USER_MODEL_NAME = environ.get('FLASK_USER_MODEL_NAME', 'User')

    # flask configuration
    SECRET_KEY = environ.get('SECRET_KEY', '123456789')
    SECURITY_SALT = environ.get('SECURITY_SALT', '123456789')

    # Email configuration
    MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = False

    MAIL_USERNAME =  environ.get('MAIL_USERNAME', 'hoovada.test@gmail.com')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD', '')

    AUTHENTICATION_MAIL_SENDER =  'Hoovada - Kết nối' 
    NOTIFICATION_MAIL_SENDER =  environ.get('NOTIFICATION_MAIL_SENDER', MAIL_DEFAULT_SENDER)

    # need to set this so that email can be sent
    MAIL_SUPPRESS_SEND = False
    TESTING = False

    # mysql configuration
    DB_USER = environ.get('DB_USER', 'dev')
    DB_PASSWORD = environ.get('DB_PASSWORD', 'hoovada')
    DB_HOST = environ.get('DB_HOST', 'localhost')
    DB_PORT = environ.get('DB_PORT', '3306')
    DB_NAME = environ.get('DB_NAME', 'hoovada')
    DB_CHARSET = 'utf8mb4'
    BCRYPT_LOG_ROUNDS = 13 # Number of times a password is hashed
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Redis configuration
    REDIS_PORT = environ.get('REDIS_PORT', '6379')
    REDIS_HOST = environ.get('REDIS_HOST', '127.0.0.1')
    REDIS_USER = environ.get('REDIS_USER', '')
    REDIS_PASSWORD = environ.get('REDIS_PASSWORD', '')
    REDIS_URL = 'redis://:' + REDIS_PASSWORD + '@' + environ.get('REDIS_URL', REDIS_HOST + ':' + REDIS_PORT)
    # The maximum number of questions/articles seen by user that will be stored on the database
    MAX_SEEN_CACHE = 10

    # Wasabi service
    S3_BUCKET = environ.get('S3_BUCKET', 'hoovada') # test bucket
    WASABI_ACCESS_KEY = environ.get('WASABI_ACCESS_KEY', '') # test bucket
    WASABI_SECRET_ACCESS_KEY = environ.get('WASABI_SECRET_ACCESS_KEY', '')  


    # RabbitMQ configuration
    RABBITMQ_PORT = environ.get('RABBITMQ_PORT', '32520')
    RABBITMQ_HOST = environ.get('RABBITMQ_HOST', '127.0.0.1')
    RABBITMQ_USER = environ.get('RABBITMQ_USER', '')
    RABBITMQ_PASSWORD = environ.get('RABBITMQ_PASSWORD', '')
    RABBITMQ_URL = 'amqp://' + RABBITMQ_USER + ':' + RABBITMQ_PASSWORD + '@' + environ.get('RABBITMQ_URL',  RABBITMQ_HOST + ':' + RABBITMQ_PORT)

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
    TWILIO_ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID', 'AC3bc87a9ca0dc5bcc55c263b00bd583c1')
    TWILIO_AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN', 'b2e699d59ef37fb757260178cdf1e3bb') # TEST Credentials
    # (create one here https://www.twilio.com/console/verify/services)
    VERIFICATION_SID = environ.get('VERIFICATION_SID', 'VAc2d0ecc3630b615db53742c8ef825fbd')
    LIMIT_VERIFY_SMS_TIME = 60 # 60seconds

    # The maximum number of questions/articles seen by user that will be stored on the database
    MAX_SEEN_CACHE = 10
    
    # OneSignal Client Configurations
    ONESIGNAL_APP_ID = environ.get('ONESIGNAL_APP_ID', '63d2ac15-58eb-49b0-b81e-a8b4582bd386')
    ONESIGNAL_REST_API_KEY = environ.get('ONESIGNAL_REST_API_KEY', 'YWI1YTE4ZWUtNDU4Yi00MTdlLThjMzItMDE3YjA0ZDI0MjQ3')
    ONESIGNAL_USER_AUTH_KEY = environ.get('ONESIGNAL_USER_AUTH_KEY', 'MGYxMDk1NmItYzRhMS00NGZkLWEyNmItZmY2MjdjZGJjZDA1')

    JSON_AS_ASCII = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
        charset=DB_CHARSET
    )

    DB_SLAVE_USER = environ.get('DB_SLAVE_USER', DB_USER)
    DB_SLAVE_PASSWORD = environ.get('DB_SLAVE_PASSWORD', DB_PASSWORD)
    DB_SLAVE_HOST = environ.get('DB_SLAVE_HOST', DB_HOST)
    DB_SLAVE_PORT = environ.get('DB_SLAVE_PORT', DB_PORT)

    SQLALCHEMY_DATABASE_SLAVE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
        user=DB_SLAVE_USER,
        password=DB_SLAVE_PASSWORD,
        host=DB_SLAVE_HOST,
        port=DB_SLAVE_PORT,
        name=DB_NAME,
        charset=DB_CHARSET
    )

class CommonDevelopmentConfig(CommonBaseConfig):
    """Development configuration."""

    MAIL_ADMINS = ['hoovada.test@gmail.com'] # list of emails to receive error reports
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
         user=CommonBaseConfig.DB_USER,
         password=CommonBaseConfig.DB_PASSWORD,
         host=CommonBaseConfig.DB_HOST,
         port=CommonBaseConfig.DB_PORT,
         name=CommonBaseConfig.DB_NAME,
         charset=CommonBaseConfig.DB_CHARSET
     )


class CommonProductionConfig(CommonBaseConfig):
    """Production configuration."""

    MAIL_ADMINS = ['admin@hoovada.com'] # list of emails to receive error reports
    DEBUG = False
    
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset={charset}'.format(
         user=CommonBaseConfig.DB_USER,
         password=CommonBaseConfig.DB_PASSWORD,
         host=CommonBaseConfig.DB_HOST,
         port=CommonBaseConfig.DB_PORT,
         name=CommonBaseConfig.DB_NAME,
         charset=CommonBaseConfig.DB_CHARSET
     )


config_by_name = dict(
    development=CommonDevelopmentConfig,
    production=CommonProductionConfig
)

key = CommonBaseConfig.SECRET_KEY
