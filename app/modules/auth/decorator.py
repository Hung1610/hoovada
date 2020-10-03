#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from functools import wraps

# third-party modules
from flask import request

# own modules
from app import db
from app.modules.auth.auth_controller import AuthController
from app.utils.response import send_error
from app.utils.types import UserRole

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


def get_entity(table_name, object_id):
    if table_name is None or object_id is None:
        return False, send_error(message='Must provide table_name and object_id')
    table_class = db.get_model_by_tablename(table_name)
    if table_class is None:
        return False, send_error(message='Table not found', code=404)
    query = table_class.query
    entity = query.get(object_id)
    if not entity:
        return False, send_error(message='Object not found', code=404)
    if not entity:
        return False, send_error(message='Object not found', code=404)
    return True, entity


def is_not_owner(table_name, object_id_arg_name, creator_field_name):
    """ Check the current user is NOT the owner of the database object.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            object_id = kwargs.get(object_id_arg_name)
            user, message = AuthController.get_logged_user(request)
            if user is None:
                return f(*args, **kwargs)
            print(table_name, object_id)
            status, result = get_entity(table_name, object_id)
            if not status:
                return result
            creator = getattr(result, creator_field_name)
            if creator == user:
                return send_error(message='User must not be owner', code=403)
            return f(*args, **kwargs)
        return decorated
    return decorator


def is_owner(table_name, object_id_arg_name, creator_field_name):
    """ Check the current user is the owner of the database object.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            object_id = kwargs.get(object_id_arg_name)
            user, message = AuthController.get_logged_user(request)
            if user is None:
                return f(*args, **kwargs)
            status, result = get_entity(table_name, object_id)
            if not status:
                return result
            creator = getattr(result, creator_field_name)
            if creator != user:
                return send_error(message='User must be owner', code=403)
            return f(*args, **kwargs)
        return decorated
    return decorator


def token_required(f):
    """ Check token for further actions.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        user, message = AuthController.get_logged_user(request)
        if user is None:
            return send_error(message=message, code=401)
        return f(*args, **kwargs)

    return decorated

# NOTE: Implement this completely, and make sure it's working before merging to master branch.
# def admin_token_required(f=None, role=None):
#     def admin_token_required_internal(f):
#         @wraps(f)
#         def decorated(*args, **kwargs):
#             user, message = AuthController.get_logged_user(request)
#             if user is None:
#                 return send_error(message=message)
#             if role is None:
#                 if not UserRole.is_admin(role=user.admin):
#                     return send_error(message='You are not admin. You need admin right to perform this action.')
#             else:
#                 if not UserRole.is_permission(role_default=role, role=user.admin):
#                     return send_error(message='You are not admin. You need admin right to perform this action.')
#             return f(*args, **kwargs)

#         return decorated

#     if f:
#         return admin_token_required_internal(f)
#     return admin_token_required_internal

def admin_token_required(f=None, role=None):
    def admin_token_required_decorator(f):
        """ Check admin rights for further actions.
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            user, message = AuthController.get_logged_user(request)
            if user is None:
                return send_error(message=message, code=401)
            if not user.admin:
                return send_error(message='You are not admin. You need admin right to perform this action.', code=403)
            return f(*args, **kwargs)
