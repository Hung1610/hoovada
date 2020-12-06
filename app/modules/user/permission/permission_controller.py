#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
import dateutil.parser

# third-party modules
from flask_restx import marshal
from sqlalchemy import and_, desc, func, or_

# own modules
from common.db import db
from app.modules.user.permission.permission_dto import PermissionDto
from common.controllers.controller import Controller
from common.utils.response import send_error, send_result
from common.utils.types import PermissionType


Permission = db.get_model('Permission')


class PermissionController(Controller):
    def create_permissions(self):
        try:
            for permission_name in PermissionType.permission_all():
                permission = Permission.query.filter(Permission.permission_name == permission_name).first()
                if not permission:  # the permission does not exist
                    permission = Permission(permission_name=permission_name)
                    db.session.add(permission)
                    db.session.commit()
        except Exception as e:
            print(e.__str__())
            pass

    def create(self, data):
        pass

    def get(self):
        try:
            permissions = Permission.query.all()
            return send_result(data=marshal(permissions, PermissionDto.model_response), message='Success')
        except Exception as e:
            print(e.__str__())
            return send_error("Could not load error, please try again later.")

    def update(self, object_id, data):
        pass

    def delete(self, object_id):
        pass

    def get_by_id(self, object_id):
        if object_id is None:
            return send_error("Permission ID is null")
        permission = Permission.query.filter_by(id=object_id).first()
        if permission is None:
            return send_error(message="Could not find permission by this ID {}".format(object_id))
        else:
            return send_result(data=marshal(permission, PermissionDto.model_response), message='Success')

    def _parse_permission(self, data, permission=None):
        pass
