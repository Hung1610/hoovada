#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.user.user_employment.user_employment_controller import EmploymentController
from app.modules.user.user_employment.user_employment_dto import EmploymentDto
from common.utils.decorator import token_required

api = EmploymentDto.api
employment_request = EmploymentDto.model_request
employment_response = EmploymentDto.model_response
parser = EmploymentDto.parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/me/employment')
class EmploymentMeList(Resource):
    @token_required
    @api.response(code=200, model=employment_response, description='Model for employment response.')
    def get(self):
        """Get all employment information of logged-in user"""

        args = get_parser.parse_args()
        controller = EmploymentController()
        user_id = g.current_user.id
        return controller.get(user_id=user_id, args=args)

    @token_required
    @api.expect(employment_request)
    @api.response(code=200, model=employment_response, description='Model for employment response.')
    def post(self):
        """ Create employment information for logged-in user"""

        data = api.payload
        controller = EmploymentController()
        return controller.create(data=data)


@api.route('/<int:user_id>/employment')
class EmploymentList(Resource):
    @api.response(code=200, model=employment_response, description='Model for employment response.')
    def get(self, user_id):
        """Get all employment information by user_id"""

        args = get_parser.parse_args()
        controller = EmploymentController()
        return controller.get(user_id=user_id, args=args)


@api.route('/all/employment/<int:id>')
class EmploymentAll(Resource):

    @token_required
    @api.expect(employment_request)
    @api.response(code=200, model=employment_response, description='Model for employment response.')
    def patch(self, id):
        """Update existing employment information by user employment id"""

        data = api.payload
        controller = EmploymentController()
        return controller.update(object_id=id, data=data)


    @token_required
    def delete(self, id):
        """Delete existing user employment information by user employment id"""

        controller = EmploymentController()
        return controller.delete(object_id=id)
