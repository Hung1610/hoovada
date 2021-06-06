#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource

# own modules
from app.modules.organization.user.user_controller import OrganizationUserController
from app.modules.organization.user.user_dto import OrganizationUserDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

api = OrganizationUserDto.api
model_organization_user_response = OrganizationUserDto.model_organization_user_response
get_list_request_parser = OrganizationUserDto.get_list_request_parser
update_status_request_parser = OrganizationUserDto.update_status_request_parser

@api.route('/<int:organization_id>/user')
class OrganizationUserList(Resource):
    @token_required
    @api.response(code=200, model=model_organization_user_response, description='Model for organization user response.')
    def post(self, organization_id):
        """Add a user to a organization"""

        controller = OrganizationUserController()
        return controller.create(object_id=organization_id)
    
    @token_required
    @api.response(code=200, model=model_organization_user_response, description='Model for organization user response.')
    def get(self, organization_id):
        """Get the list of users who joined the organization"""

        args = get_list_request_parser.parse_args()
        controller = OrganizationUserController()
        return controller.get(organization_id=organization_id, args=args)    

@api.route('/all/user/<int:id>')
class OrganizationUser(Resource):
    @token_required
    @api.response(code=200, model=model_organization_user_response, description='Model for organization user response.')
    @api.expect(update_status_request_parser)
    def patch(self, id):
        """Update status of a OrganizationUser. You must be admin or the owner of the organization to perform this action"""

        args = update_status_request_parser.parse_args()
        controller = OrganizationUserController()
        return controller.update(object_id=id, data=args)

    @token_required
    def delete(self, id):
        """Delete existing organization user by id"""

        controller = OrganizationUserController()
        result = controller.delete(object_id=id)
        return result