#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.user.user_permission.user_permission_controller import \
    UserPermissionController
# own modules
from app.modules.user.user_permission.user_permission_dto import \
    UserPermissionDto
from common.utils.decorator import admin_token_required, token_required
from common.utils.types import UserRole

api = UserPermissionDto.api
user_permission_request = UserPermissionDto.model_request
user_permission_response = UserPermissionDto.model_response

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('')
class UserPermissions(Resource):
    @token_required
    def get(self):
        pass

    @admin_token_required(role=[UserRole.SUPER_ADMIN])
    @api.expect(user_permission_request)
    @api.response(code=200, model=user_permission_response, description='Model for user permission response.')
    def post(self):
        data = api.payload
        controller = UserPermissionController()
        return controller.create(data)


@api.route('/<string:user_name>')
class UserPermission(Resource):
    @admin_token_required()
    @api.response(code=200, model=user_permission_response, description='Model for user permission response.')
    def get(self, user_name):
        controller = UserPermissionController()
        return controller.get_by_user_name(user_name)

    @admin_token_required()
    @api.expect(user_permission_request)
    @api.response(code=200, model=user_permission_response, description='Model for user permission response.')
    def post(self, user_name):
        data = api.payload
        controller = UserPermissionController()
        return controller.create_permission_for_user_name(user_name, data)
