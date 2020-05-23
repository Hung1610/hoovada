from functools import wraps

from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error

from flask import request


def token_required(f):
    """
    Check token for further actions.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        user, message = AuthController.get_logged_user(request)
        if user is None:
            return send_error(message=message)
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    '''
    Check admin rights for further actions.

    :param f:
    :return:
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        user, message = AuthController.get_logged_user(request)
        if user is None:
            return send_error(message=message)
        if not user.is_admin():
            return send_error(message='You are not admin. You need admin right to perform this action.')
        return f(*args, **kwargs)

    return decorated
