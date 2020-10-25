#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

# own modules
from app.modules.user.permission.permission import Permission
from app.modules.user.user_permission.user_permission import UserPermission
from app import db


def has_permission(user_id, permission_name):
    permission = db.session.query(UserPermission) \
        .join(Permission, Permission.id == UserPermission.permission_id) \
        .filter(Permission.permission_name == permission_name)\
        .filter(UserPermission.user_id == user_id)\
        .first()
    return permission.allow if permission is not None else True
