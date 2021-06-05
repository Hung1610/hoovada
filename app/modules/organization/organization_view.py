#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource

# own modules
from app.modules.organization.organization_controller import OrganizationController
from app.modules.organization.organization_dto import OrganizationDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = OrganizationDto.api
post_request_parser = OrganizationDto.post_request_parser
model_organization_response = OrganizationDto.model_organization_response
get_list_request_parser = OrganizationDto.get_list_request_parser
update_status_request_parser = OrganizationDto.update_status_request_parser


@api.route('')
class OrganizationList(Resource):
    @token_required
    @api.expect(post_request_parser)
    @api.response(code=200, model=model_organization_response, description='Model for organization response.')
    def post(self):
        """ Create new organization"""

        data = api.payload
        controller = OrganizationController()
        return controller.create(data=data)

    @token_required
    @api.expect(get_list_request_parser)
    @api.response(code=200, model=model_organization_response, description='Model for organization response.')
    def get(self):
        """Get the list of companies"""

        args = get_list_request_parser.parse_args()
        controller = OrganizationController()
        return controller.get(args=args)

@api.route('/<int:id>')
class Organization(Resource):
    @token_required
    @api.response(code=200, model=model_organization_response, description='Model for organization response.')
    def get(self, id):
        """Get a organization"""

        controller = OrganizationController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(post_request_parser)
    @api.response(code=200, model=model_organization_response, description='Model for organization response.')
    def patch(self, id):
        """Update the existing organization by organization id"""

        data = api.payload
        controller = OrganizationController()
        result = controller.update(object_id=id, data=data)
        return result

    @token_required
    def delete(self, id):
        """Delete existing organization by organization id"""

        controller = OrganizationController()
        result = controller.delete(object_id=id)
        return result

@api.route('/<int:id>/status')
class OrganizationStatus(Resource):
    @token_required
    @api.expect(update_status_request_parser)
    @api.response(code=200, model=model_organization_response, description='Model for organization response.')
    def patch(self, id):
        """Update the status of organization by organization id. You must be admin to perform this action"""

        data = api.payload
        controller = OrganizationController()
        result = controller.update_status(object_id=id, data=data)
        return result