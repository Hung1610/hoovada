from datetime import datetime

from flask_restx import marshal

from app import db
from app.modules.user.blacklist import BlacklistToken
from app.modules.user.user import User
from app.modules.user.user_dto import UserDto
# from app.utils.hoovada_utils import send_email
from app.utils.response import send_error, send_result
from app.utils.util import send_confirmation_email, confirm_token, decode_auth_token, encode_auth_token


def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert token
        db.session.add(blacklist_token)
        db.session.commit()
        return send_result(message='Successfully logged out.')
    except Exception as e:
        db.session.rollback()
        return send_error(message=e)


# def generate_confirmation_token(email):
#     """Confirmation email token"""
#     serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
#     return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
#
#
# def confirm_token(token, expiration=3600):
#     """Plausibility check of confirmation token."""
#     serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
#     try:
#         email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration)
#     except:
#         return False
#     return email
#
#
# def send_confirmation_email(to):
#     """Send a confirmation email to the registered user"""
#     token = generate_confirmation_token(email=to)
#     confirm_url = url_for('confirmationview', token=token, _external=True)
#     html = render_template('app/templates/confirmation.html', confirm_url=confirm_url)
#     # send_email(subject='Email confirmation', sender=Config.MAIL_DEFAULT_SENDER, recipients=to, html_body=html)


def get_id(user_id, role):
    pass


class AuthController:
    """
    This class is used to authenticate and authorize the user.
    """

    @staticmethod
    def check_user_exist(email):
        '''
        Check user exist by its email. One email on one register
        :param email:
        :return:
        '''
        # password_hash = generate_password_hash(password=password)
        user = User.query.filter_by(email=email).first()
        if user is not None:  # user is exist.
            return True
        else:
            return False

    # @staticmethod
    def register(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary form. Try again.')
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message="Please provide an email")
        if not 'password' in data or str(data['password']).strip().__eq__(''):
            return send_error(message='Pleases provide a password.')
        display_name = ''
        if 'display_name' in data:
            display_name = data['display_name']
        email = data['email']
        password = data['password']
        if AuthController.check_user_exist(email=email):
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
            db.session.rollback()
        if is_confirmed:
            try:
                send_confirmation_email(to=user.email)
                return send_result(message='An email has sent to your mailbox. Please check your email to confirm.')
            except Exception as e:
                print(e.__str__())
                return send_error(message='Could not send a confirmation email to your mailbox.')

    # @staticmethod
    def resend_confirmation(self, data):
        if not isinstance(data, dict):
            return send_error(message='Data is not correct or not in dictionary format. Try again.')
        if not 'email' in data or str(data['email']).strip().__eq__(''):
            return send_error(message="Please provide an email")
        email = data['email']
        if not AuthController.check_user_exist(email=email):
            return send_error(message='User is not registered.')
        try:
            send_confirmation_email(to=email)
            return send_result(message='An email has sent to your mailbox. Please check your email to confirm.')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not send a confirmation email to your mailbox.')

    # @staticmethod
    def confirm_email(self, token):
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user:
            if user.confirmed:
                return 'Tài khoản email đã được kích hoạt trước đó, vui lòng đăng nhập.'
            user.confirmed = True
            # user.active = True
            # user.email_confirmed = True
            user.email_confirmed_at = datetime.now()
            db.session.commit()
            return "Tài khoản email của bạn đã được kích hoạt. Vui lòng đăng nhập." #'Your email has been activated. Please login.'  # send_result(message='Account confirmation was successfully.')
        else:
            return "Mã kích hoạt của bạn không đúng hoặc đã hết hạn. Vui lòng vào trang Web <a>hoovada.com</a> để yêu cầu mã xác thực mới." #'Invalid confirmation token.'

    # @staticmethod
    def login_user(self, data):
        """
        Login user handling.
        """
        try:
            # print(data)
            user = User.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                if not user.confirmed:
                    self.resend_confirmation(data=data)
                    return send_error(message='Tài khoản email của bạn chưa được xác nhận. Vui lòng đăng nhập hộp thư của bạn để tiến hành xác thực (Trong trường hợp không thấy thư kích hoạt trong hộp thư đến, vui long kiểm tra mục thư rác).')
                auth_token = encode_auth_token(user_id=user.id)
                user.active = True
                db.session.commit()
                # if user.blocked:
                #     return None  # error(message='User has been blocked')
                if auth_token:
                    return {'access_token': auth_token.decode('utf8')}
                    # return send_result(message=auth_token)  # user
            else:
                return send_error(message='Email or Password does not match')
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not login, please try again later. Error {}'.format(e.__str__()))

    # @staticmethod
    def logout_user(self, req):
        '''
        Logout user handling.
        '''
        auth_token = None
        api_key = None
        # auth = False
        if 'X-API-KEY' in req.headers:
            api_key = req.headers['X-API-KEY']
        if 'Authorization' in req.headers:
            auth_token = req.headers.get('Authorization')
        if not auth_token and not api_key:
            # auth = False
            return None
        if api_key is not None:
            auth_token = api_key
        if auth_token:
            # get user information, check user exist
            user_id, _ = decode_auth_token(auth_token=auth_token)
            user = User.query.filter_by(id=user_id).first()
            if user is not None:
                user.active = False
                user.last_seen = datetime.now()
                db.session.commit()
            # save token to backlist.
            save_token(token=auth_token)
            return send_result(message='You are logged out.')
            # return redirect('') # to logout page
        else:
            return send_error(message='Provide a valid auth token')

    def get_user_info(self, req):
        '''
        Get user information.

        :param req: The request to handle.

        :return:
        '''
        user, message = AuthController.get_logged_user(req=req)
        if user is None:
            return send_error(message=message)
        return send_result(data=marshal(user, UserDto.model), message='Success')

    @staticmethod
    def get_logged_user(req):
        '''
        User information retrieving.
        '''
        auth_token = None
        api_key = None
        # auth = False
        if 'X-API-KEY' in req.headers:
            api_key = req.headers['X-API-KEY']
        if 'Authorization' in req.headers:
            auth_token = req.headers.get('Authorization')
        if not auth_token and not api_key:
            # auth = False
            return None, 'You must provide a valid token to continue.'
        if api_key is not None:
            auth_token = api_key
        user_id, message = decode_auth_token(auth_token=auth_token)
        if user_id is None:
            return None, message
        try:
            user = User.query.filter_by(id=user_id).first()
            return user, None
        except Exception as e:
            print(e.__str__())
            return None, message

        # auth_token = new_request.headers.get('Authorization')
        # if auth_token:
        #     auth_token = auth_token.split(' ')[1]
        #     resp = User.decode_auth_token(auth_token)
        #     if not isinstance(resp, str):
        #         user = User.query.filter_by(user_id=resp).first()
        #         return user  # tra lai JSON tương ứng về các roles đang thực hiện và các orders.
        #         # # print(user)
        #         # res = {
        #         #         'user_id': user.user_id,
        #         #         'email': user.email,
        #         #         'role': user.role,
        #         #         'name': user.name
        #         #         }
        #         # return result(data=res)
        #     return None  # error(message=resp)
        # else:
        #     return None  # error(message='Provide a valid auth token')
