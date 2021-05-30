#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.admin.career.career_controller import CareerController
from app.modules.admin.career.career_dto import CareerDto
from common.utils.decorator import admin_token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = CareerDto.api
_career_dto_request = CareerDto.model_career_request
_career_dto_response = CareerDto.model_career_response
_career_get_params = CareerDto.model_get_parser

@api.route('')
class CareerList(Resource):
    @api.response(code=200, model=_career_dto_response, description='Model for career response.')
    @api.expect(_career_get_params)
    def get(self):
        """Get all careers that satisfy conditions"""

        args = _career_get_params.parse_args()
        controller = CareerController()
        return controller.get(args=args)


    @admin_token_required
    @api.expect(_career_dto_request)
    @api.response(code=200, model=_career_dto_response, description='Model for career response.')
    def post(self):
        """Create new career"""

        data = api.payload
        controller = CareerController()
        return controller.create(data=data)

@api.route('/<string:id_or_slug>')
class Career(Resource):
    @api.response(code=200, model=_career_dto_response, description='Model for career response.')
    def get(self, id_or_slug):
        """Get an career by career id or slug"""

        controller = CareerController()
        return controller.get_by_id(object_id=id_or_slug)

    @admin_token_required
    @api.expect(_career_dto_request)
    @api.response(code=200, model=_career_dto_response, description='Model for career response.')
    def patch(self, id_or_slug):
        """Update existing career by career Id or slug"""

        data = api.payload
        controller = CareerController()
        result = controller.update(object_id=id_or_slug, data=data)
        return result


    @admin_token_required
    def delete(self, id_or_slug):
        """ Delete the career by career Id or slug"""

        controller = CareerController()
        result = controller.delete(object_id=id_or_slug)
        return result
