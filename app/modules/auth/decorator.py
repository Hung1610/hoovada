#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from functools import wraps

# third-party modules
from flask import request

# own modules
from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def token_required(f):
    """ Check token for further actions.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        user, message = AuthController.get_logged_user(request)
        if user is None:
            return send_error(message=message)
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    ''' Check admin rights for further actions.
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        user, message = AuthController.get_logged_user(request)
        if user is None:
            return send_error(message=message)
        if not user.admin:
            return send_error(message='You are not admin. You need admin right to perform this action.')
        return f(*args, **kwargs)

    return decorated
