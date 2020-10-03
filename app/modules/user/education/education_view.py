#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse
from flask import request

# own modules
# from app.modules.common.decorator import token_required
from app.modules.auth.auth_controller import AuthController
from app.modules.user.education.education_dto import EducationDto
from app.modules.user.education.education_controller import EducationController
from app.modules.auth.decorator import admin_token_required, token_required
from app.utils.response import send_error

api = EducationDto.api
education_response = EducationDto.model_response
education_request = EducationDto.model_request
get_parser = EducationDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/<int:user_id>/education')
class EducationList(Resource):
    @admin_token_required()
    @api.expect(get_parser)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def get(self, user_id):
        """
        Search all educations that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = EducationController()
        return controller.get(user_id=user_id, args=args)

    @admin_token_required()
    @api.expect(education_request)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def post(self, user_id):
        """
        Create new education.

        :return: The new education if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = EducationController()
        return controller.create(data=data, user_id=user_id)


@api.route('/me/education')
class EducationMeList(Resource):
    @token_required
    @api.response(code=200, model=education_response, description='Model for education response.')
    def get(self):
        """
        Search all educations that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = EducationController()

        current_user, _ = AuthController.get_logged_user(request)
        user_id = current_user.id

        return controller.get(user_id=user_id, args=args)

    @token_required
    @api.expect(education_request)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def post(self):
        """
        Create new education.

        :return: The new education if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = EducationController()

        current_user, _ = AuthController.get_logged_user(request)
        user_id = current_user.id

        return controller.create(data=data, user_id=user_id)


@api.route('/all/education')
class EducationAllList(Resource):
    @token_required
    @api.expect(get_parser)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def get(self):
        """
        Get all education.
        """
        args = get_parser.parse_args()
        controller = EducationController()
        return controller.get(args=args)


@api.route('/all/education/<int:id>')
class EducationAll(Resource):
    @token_required
    @api.response(code=200, model=education_response, description='Model for education response.')
    def get(self, id):
        """
        Get education by its ID.

        :param id: The ID of the education.

        :return: The education with the specific ID.
        """
        controller = EducationController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(education_request)
    @api.response(code=200, model=education_response, description='Model for education response.')
    def put(self, id):
        """
        Update existing education by its ID.

        :param id: The ID of the education which need to be updated.

        :return: The updated education if success and null vice versa.
        """
        data = api.payload
        controller = EducationController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete education by its ID.

        :param id: The ID of the education.

        :return:
        """
        controller = EducationController()
        return controller.delete(object_id=id)
