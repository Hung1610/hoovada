import os


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('FLASK_SECRET', 'f495b66803a6512d')
    SECURITY_SALT = os.environ.get('FLASK_SALT', '14be1971fc014f1b84')
    # SECRET_KEY = '~y2cS[CN}cQ:kYyY[uF{[S#p?Goo]]$f(fG3WT1f/$qJA8^%#}lMkas<Igz8&NqkizV~}})f^e3U(gsPmjAv;rw9#oN&xyXy7v>UtwXpv[h!<~8YCdkHJ7C^[Ul<<yt/'
    # SECURITY_SALT = 'jjp~%te9b*}yUdw1JPuHBUR(!K]Os@?5~eGIMH*gQaS%g^[7ufkVpFrZ8Bu&4yh/O}tNm4lpjhGCRHOvdiegM@?UEpdydj7}ESjJq£H£byFbL$A>lLrLwtC<Y8Hx}0i?ub^p@FhWYNuC:/uHM7#x*(L{T2!Jpz#TGyQd2I*6Id>e9£$iBzVLI6R[G4z*~(4D0h<VQPRA}TA21SAyr@@iJIpJS5/Rxm6}F{[uBZ~TFrP~eDlsvs1m5s4IjM^C6&F?'

    APP_DIR = os.path.abspath(
        os.path.dirname(os.path.dirname(__file__)))  # os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static')
    #IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'images')
    IMAGE_FOLDER = '/images'
    AVATAR_FOLDER = os.path.join(IMAGE_FOLDER, 'avatars')

    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME =  'admin@hoovada.com'
    MAIL_PASSWORD = 
    MAIL_DEFAULT_SENDER ='admin@hoovada.com'

    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    WASABI_ACCESS_KEY = 
    WASABI_SECRET_ACCESS_KEY = 


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = #'mysql+pymysql://<name>:<pass>@<dp ip>:<db port>/<db name>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ENV = 'dev'
    # DB_NAME = 'dev.db'
    # # Put the db file in project root
    # DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False
    # DB_NAME = 'prod.db'
    # DB_PATH = os.path.join(Config.PROJECT_ROOT, 'data', DB_NAME)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    # DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
