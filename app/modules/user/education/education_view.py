#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from flask_restx import Resource, reqparse

# own modules
from app.modules.user.education.education_controller import EducationController
from app.modules.user.education.education_dto import EducationDto
from common.utils.decorator import token_required

api = EducationDto.api
education_response = EducationDto.model_response
education_request = EducationDto.model_request
get_parser = EducationDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/me/education')
class EducationMeList(Resource):
    @token_required
    @api.response(code=200, model=education_response, description='Model for education response.')
    def get(self):
        """Get all education information of logged-in user"""

        args = get_parser.parse_args()
        controller = EducationController()
        user_id = g.current_user.id
        return controller.get(user_id=user_id, args=args)


    @token_required
    @api.expect(education_request)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def post(self):
        """Create new education information for logged-in user"""
        
        data = api.payload
        controller = EducationController()
        user_id = g.current_user.id
        return controller.create(data=data, user_id=user_id)


@api.route('/<int:user_id>/education')
class EducationList(Resource):
    @api.expect(get_parser)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def get(self, user_id):
        """Get all educations using user_id"""

        args = get_parser.parse_args()
        controller = EducationController()
        return controller.get(user_id=user_id, args=args)


@api.route('/all/education/<int:id>')
class EducationAll(Resource):

    @token_required
    @api.expect(education_request)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def patch(self, id):
        """Update existing education by education ID"""

        data = api.payload
        controller = EducationController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete education by by education ID"""

        controller = EducationController()
        return controller.delete(object_id=id)
