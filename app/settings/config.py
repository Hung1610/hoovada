import os
import logging


class BaseConfig:
    # debug mode is turned off by default
    DEBUG = False

    # flask configuration
    SECRET_KEY = os.environ.get('FLASK_SECRET')
    SECURITY_SALT = os.environ.get('FLASK_SALT')
    # SECRET_KEY = '~y2cS[CN}cQ:kYyY[uF{[S#p?Goo]]$f(fG3WT1f/$qJA8^%#}lMkas<Igz8&NqkizV~}})f^e3U(gsPmjAv;rw9#oN&xyXy7v>UtwXpv[h!<~8YCdkHJ7C^[Ul<<yt/'
    # SECURITY_SALT = 'jjp~%te9b*}yUdw1JPuHBUR(!K]Os@?5~eGIMH*gQaS%g^[7ufkVpFrZ8Bu&4yh/O}tNm4lpjhGCRHOvdiegM@?UEpdydj7}ESjJq£H£byFbL$A>lLrLwtC<Y8Hx}0i?ub^p@FhWYNuC:/uHM7#x*(L{T2!Jpz#TGyQd2I*6Id>e9£$iBzVLI6R[G4z*~(4D0h<VQPRA}TA21SAyr@@iJIpJS5/Rxm6}F{[uBZ~TFrP~eDlsvs1m5s4IjM^C6&F?'

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = False
    MAIL_USERNAME =  os.environ.get('MAIL_USERNAME', 'admin@hoovada.com')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME', 'admin@hoovada.com') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@hoovada.com'] # list of emails to receive error reports

    # Wasabi service
    WASABI_ACCESS_KEY = os.environ.get('WASABI_ACCESS_KEY')
    WASABI_SECRET_ACCESS_KEY = os.environ.get('WASABI_SECRET_ACCESS_KEY')

    # mysql configuration
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT', '3360')
    DB_NAME = os.environ.get('DB_NAME', 'hoovada')

    # Locations
    APP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    IMAGE_FOLDER = '/images'
    AVATAR_FOLDER = os.path.join(IMAGE_FOLDER, 'avatars')

    # other configurations
    BCRYPT_LOG_ROUNDS = 13 # Number of times a password is hashed
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # logging
    LOG_FILENAME = 'hoovada.log'
    LOG_MAXBYTES = 1024
    LOG_BACKUPS = 5


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_ECHO = True
    LOG_LEVEL = logging.DEBUG

    # if you want to use mysql 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'.format(
         user=BaseConfig.DB_USER,
         password=BaseConfig.DB_PASSWORD,
         host=BaseConfig.DB_HOST,
         port=BaseConfig.DB_PORT,
         name=BaseConfig.DB_NAME
     )
    
    # If you want to use sqlite for development, Put the db file in project root
    # DB_NAME = 'dev.db'
    # DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

   
class TestingConfig(BaseConfig):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"


class ProductionConfig(BaseConfig):
    """production configuration."""
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'.format(
         user=BaseConfig.DB_USER,
         password=BaseConfig.DB_PASSWORD,
         host=BaseConfig.DB_HOST,
         port=BaseConfig.DB_PORT,
         name=BaseConfig.DB_NAME
     )

    LOG_LEVEL = logging.INFO


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = BaseConfig.SECRET_KEY
