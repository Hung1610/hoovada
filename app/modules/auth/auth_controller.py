from app import db
from app.modules.user.blacklist import BlacklistToken
from app.modules.user.user import User
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


def get_id(user_id, role):
    pass


class AuthController:
    """
    This class is used to authenticate and authorize the user.
    """

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
