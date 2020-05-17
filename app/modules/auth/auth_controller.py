from flask import url_for, render_template
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

from app import db
from app.modules.user.blacklist import BlacklistToken
from app.modules.user.user import User
from app.settings import config
from app.settings.config import Config
from app.utils.hoovada_utils import send_email
from app.utils.response import send_error, send_result


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert token
        db.session.add(blacklist_token)
        db.session.commit()
        return send_result(message='Successfully logged out.')
    except Exception as e:
        return send_error(message=e)


def generate_confirmation_token(email):
    """Confirmation email token"""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    """Plausibility check of confirmation token."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration)
    except:
        return False
    return email


def send_confirmation_email(to):
    """Send a confirmation email to the registered user"""
    token = generate_confirmation_token(email=to)
    confirm_url = url_for('confirmationview', token=token, _external=True)
    html = render_template('app/templates/confirmation.html', confirm_url=confirm_url)
    send_email(subject='Email confirmation', sender=Config.MAIL_DEFAULT_SENDER, recipients=to, html_body=html)


def get_id(user_id, role):
    pass


class AuthController:
    """
    This class is used to authenticate and authorize the user.
    """

    @staticmethod
    def check_user_exist(email, password):
        password_hash = generate_password_hash(password=password)
        user = User.query.filter_by(User.email == email, User.password_hash == password_hash).first()
        if user is not None:  # user is exist.
            return True
        else:
            return False

    @staticmethod
    def register(data):
        if not isinstance(data, dict):
            return send_error(message='Please enter email and password')
        if not 'email' in data or not 'password' in data:
            return send_error(message="Please provide email and password")
        display_name = data['display_name']
        email = data['email']
        password = data['password']
        if AuthController.check_user_exist(email=email, password=password):
            return send_result(message='User already exist.')
        user = User(display_name=display_name, email=email, confirmed=False)
        user.set_password(password=password)
        try:
            # user.save()
            db.session.add(user)
            db.session.commit()
            is_confirmed = True  # if saving is successfull --> send confirmation
        except Exception as e:
            print(e.__str__())
            is_confirmed = False
        if is_confirmed:
            try:
                send_confirmation_email(to=user.email)
            except Exception as e:
                print(e.__str__())

    @staticmethod
    def confirm_email(data):
        pass

    @staticmethod
    def login_user(data):
        """
        Login user handling.
        """
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password_hash')):
                auth_token = User.encode_auth_token(user.user_id)
                if user.blocked:
                    return None  # error(message='User has been blocked')
                if auth_token:
                    # role = user.role
                    # if role.__eq__('user'):
                    #     pass

                    return user
            else:
                return None  # error(message='Email or Password does not match')
        except Exception as e:
            return send_error(message=e)

    @staticmethod
    def logout_user(data):
        '''
        Logout user handling.
        '''
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                return send_error(message=resp)
        else:
            return send_error(message='Provide a valid auth token')

    @staticmethod
    def get_logged_user(new_request):
        '''
        User information retrieving.
        '''
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            auth_token = auth_token.split(' ')[1]
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(user_id=resp).first()
                return user  # tra lai JSON tương ứng về các roles đang thực hiện và các orders.
                # # print(user)
                # res = {
                #         'user_id': user.user_id,
                #         'email': user.email,
                #         'role': user.role,
                #         'name': user.name
                #         }
                # return result(data=res)
            return None  # error(message=resp)
        else:
            return None  # error(message='Provide a valid auth token')
