from functools import wraps

from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error

from flask import request


def token_required(f):
    """
    [DEPRECATED]
    This function has moved to utils/auth
    """

    # @wraps(f)
    # def decorated(*args, **kwargs):
    #     token = request.headers.get('Authorization')
    #     if not token.__eq__('u6ihHxwhDEzeBcYU'):
    #         return send_error(message="Token is not correct")
    #
    #     return f(*args, **kwargs)
    #
    # return decorated

    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = AuthController.get_logged_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = AuthController.get_logged_user(request)
        token = data.get('data')

        if not token:
            return data, status

        role = token.get('role')
        if role != 3:
            return send_error('Admin token required')

        return f(*args, **kwargs)

    return decorated
