import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


# Mixins allow for maintaining code and docs across several files
class UserManagerConfigMixin(object):
    """This class contains User settings and their defaults that will be used to mix into the User class.
        """

    #: | Allow users to login and register with an email address
    USER_ENABLE_EMAIL = True

    #: | Allow users to login and register with a username
    USER_ENABLE_USERNAME = True

    #: | Allow users to change their username.
    #: | Depends on USER_ENABLE_USERNAME=True.
    USER_ENABLE_CHANGE_USERNAME = True

    #: | Allow users to change their password.
    USER_ENABLE_CHANGE_PASSWORD = True

    #: | Enable email confirmation emails to be sent.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_CONFIRM_EMAIL = True

    #: | Allow users to reset their passwords.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_ENABLE_FORGOT_PASSWORD = True

    #: | Allow unregistered users to be invited.
    USER_ENABLE_INVITE_USER = False

    #: | Allow unregistered users to register.
    USER_ENABLE_REGISTER = True

    #: Automatic sign-in if the user session has not expired.
    USER_AUTO_LOGIN = False

    #: Automatic sign-in after a user confirms their email address.
    USER_AUTO_LOGIN_AFTER_CONFIRM = True

    #: Automatic sign-in after a user registers.
    USER_AUTO_LOGIN_AFTER_REGISTER = False

    #: Automatic sign-in after a user resets their password.
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = False

    #: | Sender's email address, used by the EmailAdapters.
    #: | Required for sending emails.
    #: | Derived from MAIL_DEFAULT_SENDER or DEFAULT_MAIL_SENDER when specified.
    USER_EMAIL_SENDER_EMAIL = ''

    #: | Sender's name, user by the EmailAdapters.
    #: | Optional. Defaults to USER_APP_NAME setting.
    USER_EMAIL_SENDER_NAME = ''

    #: | Send notification email after a password change.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_PASSWORD_CHANGED_EMAIL = True

    #: | Send notification email after a registration.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_REGISTERED_EMAIL = True

    #: | Send notification email after a username change.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SEND_USERNAME_CHANGED_EMAIL = True

    #: | Only invited users may register.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_REQUIRE_INVITATION = False

    #: | Ensure that users can login only with a confirmed email address.
    #: | Depends on USER_ENABLE_EMAIL=True.
    #:
    #: This setting works in tandem with the ``@allow_unconfirmed_emails``
    #: view decorator to allow users without confirmed email addresses
    #: to access certain views.
    #:
    #: .. caution::
    #:
    #:     | Use ``USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL=True`` and
    #:         ``@allow_unconfirmed_email`` with caution,
    #:         as they relax security requirements.
    #:     | Make sure that decorated views **never call other views directly**.
    #:         Allways se ``redirect()`` to ensure proper view protection.

    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False

    #: | Show 'Email does not exist' message instead of 'Incorrect Email or password'.
    #: | Depends on USER_ENABLE_EMAIL=True.
    USER_SHOW_EMAIL_DOES_NOT_EXIST = False

    #: | Show 'Username does not exist' message instead of 'Incorrect Username or password'.
    #: | Depends on USER_ENABLE_USERNAME=True.
    USER_SHOW_USERNAME_DOES_NOT_EXIST = False
    USER_REQUIRE_RETYPE_PASSWORD = True

    #: | Email confirmation token expiration in seconds.
    #: | Default is 2 days (2*24*3600 seconds).
    USER_CONFIRM_EMAIL_EXPIRATION = 2 * 24 * 3600

    #: | Reset password token expiration in seconds.
    #: | Default is 2 days (2*24*3600 seconds).
    USER_RESET_PASSWORD_EXPIRATION = 2 * 24 * 3600

    #: | User session token expiration in seconds.
    #: | Default is 1 hour (1*3600 seconds).
    USER_USER_SESSION_EXPIRATION = 1 * 3600

    USER_CHANGE_PASSWORD_URL = '/auth/change-password'  #:
    USER_CONFIRM_EMAIL_URL = '/auth/confirm-email/<token>'  #:
    USER_UNAUTHENTICATED_URL = '/auth/unconfirmed-account'  #:
    USER_EDIT_USER_PROFILE_URL = '/user/edit-profile'  #:
    USER_FORGOT_PASSWORD_URL = '/auth/forgot-password'  #:
    USER_LOGIN_URL = '/auth/login'  #:
    USER_LOGOUT_URL = '/auth/logout'  #:
    USER_REGISTER_URL = '/auth/register'  #:
    USER_RESEND_EMAIL_CONFIRMATION_URL = '/auth/resend-email-confirmation'  #:

    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     Template file settings
    USER_RESET_PASSWORD_URL = '/user/reset-password/<token>'

    USER_CHANGE_PASSWORD_TEMPLATE = 'auth/change_password.html.j2'  #:
    USER_EDIT_USER_PROFILE_TEMPLATE = 'user/edit_user_profile.html.j2'  #:
    USER_FORGOT_PASSWORD_TEMPLATE = 'auth/forgot_password.html.j2'  #:
    USER_LOGIN_TEMPLATE = 'auth/login.html.j2'  #:
    USER_REGISTER_TEMPLATE = 'auth/register.html.j2'  #:
    USER_RESEND_CONFIRM_EMAIL_TEMPLATE = 'auth/resend_confirm_email.html.j2'  #:

    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     Email template file settings
    USER_RESET_PASSWORD_TEMPLATE = 'auth/reset_password.html.j2'

    USER_CONFIRM_EMAIL_TEMPLATE = 'emails/confirm_email'  #:
    USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'emails/password_changed'  #:
    USER_REGISTERED_EMAIL_TEMPLATE = 'emails/registered'  #:
    USER_RESET_PASSWORD_EMAIL_TEMPLATE = 'emails/reset_password'  #:

    #: .. This hack shows a header above the _next_ section
    #: .. code-block:: none
    #:
    #:     FLask endpoint settings
    USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'emails/username_changed'

    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = ''  #:
    USER_AFTER_CHANGE_USERNAME_ENDPOINT = ''  #:
    USER_AFTER_CONFIRM_ENDPOINT = ''  #:
    USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = ''  #:
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = ''  #:
    USER_AFTER_LOGIN_ENDPOINT = ''  #:
    USER_AFTER_LOGOUT_ENDPOINT = ''  #:
    USER_AFTER_REGISTER_ENDPOINT = ''  #:
    USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = ''  #:
    USER_AFTER_RESET_PASSWORD_ENDPOINT = ''  #:
    USER_AFTER_INVITE_ENDPOINT = ''  #:
    USER_UNAUTHENTICATED_ENDPOINT = 'auth.login'  #:
    USER_UNAUTHORIZED_ENDPOINT = 'auth.unauthorized'  #:
    USER_UNCONFIRMED_EMAIL_ENDPOINT = 'auth.unconfirmed'  #:


# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
#     DEBUG = False

class Config(UserManagerConfigMixin):
    # Basic Quart Settings
    BASEDIR = BASEDIR
    APP_NAME = 'hoovada'
    APP_EMAIL_ADDR_BASE = f'@{APP_NAME}.com'
    SITE_AUTHOR = 'Noi Nguyen'
    SERVER_NAME = 'localhost:5000'
    # SERVER_NAME = '167.99.66.93:5000'
    STATIC_FOLDER = os.path.join(BASEDIR, 'static')
    SECRET_KEY = '~y2cS[CN}cQ:kYyY[uF{[S#p?Goo]]$f(fG3WT1f/$qJA8^%#}lMkas<Igz8&NqkizV~}})f^e3U(gsPmjAv;rw9#oN&xyXy7v>UtwXpv[h!<~8YCdkHJ7C^[Ul<<yt/'
    SECURITY_PASSWORD_SALT = 'jjp~%te9b*}yUdw1JPuHBUR(!K]Os@?5~eGIMH*gQaS%g^[7ufkVpFrZ8Bu&4yh/O}tNm4lpjhGCRHOvdiegM@?UEpdydj7}ESjJq£H£byFbL$A>lLrLwtC<Y8Hx}0i?ub^p@FhWYNuC:/uHM7#x*(L{T2!Jpz#TGyQd2I*6Id>e9£$iBzVLI6R[G4z*~(4D0h<VQPRA}TA21SAyr@@iJIpJS5/Rxm6}F{[uBZ~TFrP~eDlsvs1m5s4IjM^C6&F?'

    # Flask-SQLAlchemy
    SQLITE_DATABASE_NAME = f'{APP_NAME}'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, SQLITE_DATABASE_NAME)
    DATABASE_USER = 'dev'
    DATABASE_PASS = 'hoovada@'
    DATABASE_NAME = f'{APP_NAME}'
    DATABASE_IP = '167.99.66.93'
    DATABASE_PORT = 1507
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_IP}:{DATABASE_PORT}/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_SIZE = 20
    DEBUG = False
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
    PRO_PIC_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # Flask-Mail
    # MAIL_SERVER = 'localhost'
    # MAIL_PORT = 8025
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = 'hoovada^0123'

    MAIL_DEFAULT_SENDER = 'hoovadateam@gmail.com'
    MAIL_DEFAULT_REPLY_TO = f'enquiries{APP_EMAIL_ADDR_BASE}'
    ADMINS = [f'admin-{APP_EMAIL_ADDR_BASE}']

    QUESTIONS_PER_PAGE = 10

    ELASTICSEARCH_URL = 'http://localhost:9200'

    LOGGING_CATEGORIES = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    LOG_TO_STDOUT = False

    LANGUAGES = ['en', 'vi']

    # WTF_CSRF_CHECK_DEFAULT = False

    # LOCATION_DB_PATH = os.path.join(BASEDIR,'../../IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN')


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
