#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from common.decorator import token_required
from app.modules.language.language_dto import LanguageDto
from app.modules.language.language_controller import LanguageController
from common.utils.decorator import token_required

api = LanguageDto.api
language_response = LanguageDto.model_response
language_request = LanguageDto.model_request
get_parser = LanguageDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/initialize')
class LanguageInitialize(Resource):
    @token_required
    @api.response(code=200, model=language_response, description='Model for language response.')
    def post(self):
        """
        Create default languages.
        """
        controller = LanguageController()
        return controller.create_languages()


@api.route('')
class LanguageList(Resource):
    @token_required
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self):
        """
        Search all languages that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = LanguageController()
        return controller.get(args=args)

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
        return controller.create(data=data)


@api.route('/<int:id>')
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
