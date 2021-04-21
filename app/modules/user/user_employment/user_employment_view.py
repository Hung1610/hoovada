#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

from app.modules.user.user_employment.user_employment_controller import \
    UserEmploymentController
# own modules
from app.modules.user.user_employment.user_employment_dto import \
    UserEmploymentDto
from common.utils.decorator import admin_token_required, token_required

api = UserEmploymentDto.api
user_employment_request = UserEmploymentDto.model_request
user_employment_response = UserEmploymentDto.model_response

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/me/employment')
class UserEmploymentList(Resource):
    @token_required
    @api.expect(user_employment_request)
    @api.response(code=200, model=user_employment_response, description='Model for question topic response.')
    def post(self):
        """ Create new user_employment."""

        data = api.payload
        controller = UserEmploymentController()
        return controller.create(data=data)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, required=True, help='Search employment by user_id')

@api.route('/all/employment')
@api.expect(parser)
class UserEmploymentSearch(Resource):
    @api.response(code=200, model=user_employment_response, description='Model for user title response.')
    def get(self):
        """ Search all employment that satisfy conditions."""
        
        args = parser.parse_args()
        controller = UserEmploymentController()
        return controller.search(args=args)

@api.route('/all/employment/<int:id>')
class UserEmploymentAll(Resource):
    @api.response(code=200, model=user_employment_response, description='Model for employment response.')
    def get(self, id):
        """Get employment by user-employment ID"""

        controller = UserEmploymentController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(user_employment_request)
    @api.response(code=200, model=user_employment_response, description='Model for employment response.')
    def put(self, id):
        """Update existing employment by user-employment ID"""
        data = api.payload
        controller = UserEmploymentController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete employment by its ID.
        """
        controller = UserEmploymentController()
        return controller.delete(object_id=id)
