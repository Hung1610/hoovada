#!/usr/bin/env python
# -*- coding: utf-8 -*-

# build-in modules
import os
from datetime import datetime
import dateutil.parser

# third-party modules
from flask import url_for, request, send_file
from flask_restx import marshal

# own modules
from app import db
from common.models import User
from app.modules.user.permission.permission import Permission
from app.modules.user.user_permission.user_permission import UserPermission
from app.modules.user.user_permission.user_permission_dto import UserPermissionDto
from common.utils.response import send_result, send_error
from common.controllers.controller import Controller
from app.constants import messages
# from app.settings.config import BaseConfig as Config
# from common.utils.util import encode_file_name
# from common.utils.types import UserRole


class UserPermissionController(Controller):
    def create(self, data):
        user_id = data.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return send_error(data=messages.ERR_NOT_FOUND_WITH_ID.format(user_id))
        if not isinstance(data, dict):
            return send_error(message='You must pass dictionary-like data.')
        try:
            permissions = data['permissions']
            for permission in permissions:
                p = Permission.query.filter_by(permission_name=permission['name']).first()
                user_permission_db = UserPermission.query \
                    .filter_by(user_id=user.id) \
                    .filter_by(permission_id=p.id).first()

                if not user_permission_db:
                    user_permission = UserPermission(user_id=user.id,
                                                     permission_id=p.id,
                                                     allow=permission.get('allow') == 1)
                    db.session.add(user_permission)
                else:
                    user_permission_db.allow = permission.get('allow') == 1
            db.session.commit()
            return send_result(message='Set user permission successfully', data=[])
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not set user permission')

    def get(self):
        pass

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def create_permission_for_user_name(self, user_name, data):
        if user_name is None:
            return send_error(message="The user_name must not be null.")
        user = User.query.filter_by(display_name=user_name).first()
        if user is None:
            return send_error(data="Could not exist user by this user name")

        if not isinstance(data, dict):
            return send_error(message='You must pass dictionary-like data.')
        if 'permission_name' not in data:
            return send_error(message='Missing field permission_name')
        permission = Permission.query.filter_by(permission_name=data['permission_name']).first()
        if permission is None:
            return send_error(data="Could not exist permission")
        try:
            user_permission_db = UserPermission.query \
                .filter_by(user_id=user.id) \
                .filter_by(permission_id=permission.id).first()

            if not user_permission_db:
                user_permission = UserPermission(user_id=user.id,
                                                 permission_id=permission.id,
                                                 allow=data.get('allow') or True)
                db.session.add(user_permission)
            else:
                user_permission_db.allow = data.get('allow')
            db.session.commit()
            return send_result(message='Set user permission successfully', data=[])
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not set user permission')

    def get_by_user_name(self, user_name):
        if user_name is None:
            return send_error(message="The user_name must not be null.")
        try:
            user_permission = (db.session.query(UserPermission, User, Permission)
                               .join(Permission, isouter=True)
                               .join(User, isouter=True)
                               .filter(User.display_name == user_name)).all()
            u_p_response = list()
            for u_p in user_permission:
                u_p_response.append({
                    'id': u_p[0].id,
                    'display_name': u_p[1].display_name,
                    'permission_name': u_p[2].permission_name,
                    'allow': u_p[0].allow,
                })
            return send_result(data=marshal(u_p_response, UserPermissionDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get user permission by user_name {}.'.format(user_name))

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error(message="The ID must not be null.")
        try:
            user_permission = UserPermission.query.filter_by(id=object_id).first()
            if user_permission is None:
                return send_error(data="Could not find user permission by this id")
            else:
                return send_result(data=marshal(user_permission, UserPermissionDto.model_response))
        except Exception as e:
            print(e.__str__())
            return send_error(message='Could not get user permission by ID {}.'.format(object_id))

    def _parse_user_permission(self, data, user_permission=None):
        pass
