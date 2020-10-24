#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse
from flask import request

# own modules
# from app.common.decorator import token_required
from app.modules.auth.auth_controller import AuthController
from app.modules.user.language.language_dto import LanguageDto
from app.modules.user.language.language_controller import LanguageController
from app.modules.auth.decorator import admin_token_required, token_required
from app.utils.response import send_error

api = LanguageDto.api
language_response = LanguageDto.model_response
language_request = LanguageDto.model_request
get_parser = LanguageDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/<int:user_id>/language')
class LanguageList(Resource):
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self, user_id):
        """
        Search all languages that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = LanguageController()
        return controller.get(user_id=user_id, args=args)

    @admin_token_required()
    @api.expect(language_request)
    @api.response(code=200, model=language_response, description='Model for language response.')
    def post(self, user_id):
        """
        Create new language.

        :return: The new language if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = LanguageController()
        return controller.create(data=data, user_id=user_id)


@api.route('/me/language')
class LanguageMeList(Resource):
    @token_required
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self):
        """
        Search all languages that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = LanguageController()

        current_user, _ = AuthController.get_logged_user(request)
        user_id = current_user.id

        return controller.get(user_id=user_id, args=args)

    @token_required
    @api.expect(language_request)
    @api.response(code=200, model=language_response, description='Model for language response.')
    def post(self):
        """
        Create new language.

        :return: The new language if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = LanguageController()

        current_user, _ = AuthController.get_logged_user(request)
        user_id = current_user.id

        return controller.create(data=data, user_id=user_id)


@api.route('/all/language')
class LanguageAllList(Resource):
    @token_required
    @api.expect(get_parser)
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self):
        """
        Get all language.
        """
        args = get_parser.parse_args()
        controller = LanguageController()
        return controller.get(args=args)


@api.route('/all/language/<int:id>')
class LanguageAll(Resource):
    @token_required
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self, id):
        """
        Get language by its ID.

        :param id: The ID of the language.

        :return: The language with the specific ID.
        """
        controller = LanguageController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(language_request)
    @api.response(code=200, model=language_response, description='Model for language response.')
    def put(self, id):
        """
        Update existing language by its ID.

        :param id: The ID of the language which need to be updated.

        :return: The updated language if success and null vice versa.
        """
        data = api.payload
        controller = LanguageController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """
        Delete language by its ID.

        :param id: The ID of the language.

        :return:
        """
        controller = LanguageController()
        return controller.delete(object_id=id)
