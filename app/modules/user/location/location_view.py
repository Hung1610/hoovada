#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import g
from flask_restx import Resource

# own modules
from app.modules.user.location.location_controller import LocationController
from app.modules.user.location.location_dto import LocationDto
from common.utils.decorator import token_required

api = LocationDto.api
location_response = LocationDto.model_response
location_request = LocationDto.model_request
get_parser = LocationDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."

@api.route('/me/location')
class LocationMeList(Resource):
    @token_required
    @api.response(code=200, model=location_response, description='Model for location response.')
    def get(self):
        """Get all location information of logged-in user"""

        args = get_parser.parse_args()
        controller = LocationController()
        user_id = g.current_user.id
        return controller.get(args=args, user_id=user_id)


    @token_required
    @api.expect(location_request)
    @api.response(code=200, model=location_response, description='Model for location response.')
    def post(self):
        """Create location information of logged-in user"""

        data = api.payload
        controller = LocationController()
        user_id = g.current_user.id
        return controller.create(data=data, user_id=user_id)


@api.route('/<int:user_id>/location')
class LocationList(Resource):
    @api.response(code=200, model=location_response, description='Model for location response.')
    def get(self, user_id):
        """Get all location information using user_id"""
        args = get_parser.parse_args()
        controller = LocationController()
        return controller.get(args=args, user_id=user_id)


@api.route('/all/location/<int:id>')
class LocationAll(Resource):
    @token_required
    @api.expect(location_request)
    @api.response(code=200, model=location_response, description='Model for location response.')
    def patch(self, id):
        """Update existing location information by location id"""

        data = api.payload
        controller = LocationController()
        return controller.update(data=data, object_id=id)

    @token_required
    def delete(self, id):
        """Delete existing location information by location id"""

        controller = LocationController()
        return controller.delete(object_id=id)
