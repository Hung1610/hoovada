from functools import wraps
from app.utils.response import send_error

from flask import request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token.__eq__('u6ihHxwhDEzeBcYU'):
            return send_error(message="Token is not correct")

        return f(*args, **kwargs)

    return decorated
