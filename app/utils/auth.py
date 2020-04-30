from functools import wraps

from functools import wraps

from flask import request

from app.utils.response import send_error


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authenticated = Auth.get_logged_in_user(request)

        if not authenticated:
            return send_error(message="User not authenticated")

        return f(*args, **kwargs)

    return decorated


class Auth:

    @classmethod
    def get_logged_in_user(cls, req):
        # auth_token = req.headers.get('Authorization')
        auth_token = None
        api_key = None
        auth = False

        if 'X-API-KEY' in request.headers:
            api_key = request.headers['X-API-KEY']
        if 'Authorization' in request.headers:
            auth_token = request.headers.get('Authorization')
        if not auth_token and not api_key:
            auth = False
        if str(auth_token).strip().__eq__('0e885a3c4c520f8a9159e1dbad7de745') or str(api_key).strip().__eq__('0e885a3c4c520f8a9159e1dbad7de745'):
            auth = True

        return auth
