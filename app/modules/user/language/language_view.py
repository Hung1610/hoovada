#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from flask_restx import Resource

# own modules
from app.modules.user.language.language_controller import LanguageController
from app.modules.user.language.language_dto import LanguageDto
from common.utils.decorator import token_required

api = LanguageDto.api
language_response = LanguageDto.model_response
language_request = LanguageDto.model_request
get_parser = LanguageDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/me/language')
class LanguageMeList(Resource):
    @token_required
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self):
        """Get all language information of logged-in user"""
        
        args = get_parser.parse_args()
        controller = LanguageController()
        user_id = g.current_user.id
        return controller.get(args=args, user_id=user_id)

    @token_required
    @api.expect(language_request)
    @api.response(code=200, model=language_response, description='Model for language response.')
    def post(self):
        """Create new language information for logged-in user"""

        data = api.payload
        controller = LanguageController()
        user_id = g.current_user.id
        return controller.create(data=data, user_id=user_id)


@api.route('/<int:user_id>/language')
class LanguageList(Resource):
    @api.response(code=200, model=language_response, description='Model for language response.')
    def get(self, user_id):
        """Get all language information by user_id"""

        args = get_parser.parse_args()
        controller = LanguageController()
        return controller.get(args=args, user_id=user_id)


@api.route('/all/language/<int:id>')
class LanguageAll(Resource):

    @token_required
    @api.expect(language_request)
    @api.response(code=200, model=language_response, description='Model for language response.')
    def patch(self, id):
        """Update existing language information by language ID"""

        data = api.payload
        controller = LanguageController()
        return controller.update(data=data, object_id=id)

    @token_required
    def delete(self, id):
        """Delete existing language information by language ID"""
        
        controller = LanguageController()
        return controller.delete(object_id=id)
