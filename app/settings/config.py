import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dev:hoovada%40@167.99.66.93:1507/hoovada'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dev:hoovada%40@167.99.66.93:1507/hoovada'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
