#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from os import environ

# third party modules
from dramatiq.brokers.rabbitmq import RabbitmqBroker

# own modules
from common.settings.config import CommonBaseConfig

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class BaseConfig(CommonBaseConfig):
    # debug mode is turned off by default
    DEBUG = False

    # Flask-Dramatiq configuration
    DRAMATIQ_BROKER = RabbitmqBroker
    DRAMATIQ_BROKER_URL = CommonBaseConfig.RABBITMQ_URL

    # Cache configuration   # Flask-Caching related configs
    # Simple cache using Python dictionary
    # CACHE_TYPE = "simple"
    # Redis cache using redis database
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'fcache'
    CACHE_REDIS_PORT = CommonBaseConfig.REDIS_PORT
    CACHE_REDIS_HOST = CommonBaseConfig.REDIS_HOST
    CACHE_REDIS_PASSWORD = CommonBaseConfig.REDIS_PASSWORD
    CACHE_REDIS_URL = CommonBaseConfig.REDIS_URL
    CACHE_DEFAULT_TIMEOUT = environ.get('CACHE_DEFAULT_TIMEOUT', 50)

    # Flask-SQLAlchemy configurations
    SQLALCHEMY_ECHO = False

    # mysql configuration
    DB_USER = environ.get('DB_USER', 'dev')
    DB_PASSWORD = environ.get('DB_PASSWORD', 'hoovada')
    DB_HOST = environ.get('DB_HOST', 'localhost')
    DB_PORT = environ.get('DB_PORT', '3306') 
    DB_NAME = environ.get('DB_NAME', 'hoovada')
    DB_CHARSET = 'utf8mb4'


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
    
    SQLALCHEMY_ECHO = False
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
