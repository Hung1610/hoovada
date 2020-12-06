#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules

# third-party modules

# own modules
from common.db import db


Permission = db.get_model('Permission')
UserPermission = db.get_model('UserPermission')


def has_permission(user_id, permission_name):
    permission = db.session.query(UserPermission) \
        .join(Permission, Permission.id == UserPermission.permission_id) \
        .filter(Permission.permission_name == permission_name)\
        .filter(UserPermission.user_id == user_id)\
        .first()
    return permission.allow if permission is not None else True
