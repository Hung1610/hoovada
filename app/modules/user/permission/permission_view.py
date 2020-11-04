#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.user.permission.permission_controller import \
    PermissionController
from app.modules.user.permission.permission_dto import PermissionDto
# own modules
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = PermissionDto.api
permission_request = PermissionDto.model_request
permission_response = PermissionDto.model_response


@api.route('/')
class Permission(Resource):
    @admin_token_required()
    @api.response(code=200, model=permission_response, description='Model for permission response.')
    def get(self):
        controller = PermissionController()
        return controller.get()

    @admin_token_required()
    @api.expect(permission_request)
    def post(self):
        controller = PermissionController()
        return controller.create()


@api.route('/create_permission')
class CreateFixedPermission(Resource):
    @admin_token_required()
    def post(self):
        controller = PermissionController()
        return controller.create_permissions()
