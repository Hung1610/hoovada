#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.user.user_employment.user_employment_dto import UserEmploymentDto
from app.modules.user.user_employment.user_employment_controller import UserEmploymentController
from app.modules.auth.decorator import admin_token_required, token_required

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
        """ 
        Create new user_employment.
        """

        data = api.payload
        controller = UserEmploymentController()
        return controller.create(data=data)


parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, required=True, help='Search employment by user_id')
parser.add_argument('is_default', type=int, required=False, help='Search default display')

@api.route('/all/employment')
@api.expect(parser)
class UserEmploymentSearch(Resource):
    @token_required
    @api.response(code=200, model=user_employment_response, description='Model for user title response.')
    def get(self):
        """ 
        Search all employment that satisfy conditions.
        
        """
        
        args = parser.parse_args()
        controller = UserEmploymentController()
        return controller.search(args=args)
