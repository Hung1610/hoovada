#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask import current_app, request
from flask_restx import Resource, reqparse

# own modules
from app.modules.user.location.location_controller import LocationController
from app.modules.user.location.location_dto import LocationDto
from common.utils.decorator import admin_token_required, token_required
from common.utils.response import send_error

api = LocationDto.api
location_response = LocationDto.model_response
location_request = LocationDto.model_request
get_parser = LocationDto.model_get_parser

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


@api.route('/<int:user_id>/location')
class LocationList(Resource):
    @api.response(code=200, model=location_response, description='Model for location response.')
    def get(self, user_id):
        """
        Search all locations that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = LocationController()
        return controller.get(user_id=user_id, args=args)

    @admin_token_required()
    @api.expect(location_request)
    @api.response(code=200, model=location_response, description='Model for location response.')
    def post(self, user_id):
        """
        Create new location.

        :return: The new location if it was created successfully and null vice versa.
        """
        data = api.payload
        controller = LocationController()
        return controller.create(data=data, user_id=user_id)


@api.route('/me/location')
class LocationMeList(Resource):
    @token_required
    @api.response(code=200, model=location_response, description='Model for location response.')
    def get(self):
        """
        Search all locations that satisfy conditions.
        """
        args = get_parser.parse_args()
        controller = LocationController()

        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id

        return controller.get(user_id=user_id, args=args)

    @token_required
    @api.expect(location_request)
    @api.response(code=200, model=location_response, description='Model for location response.')
    def post(self):
        """Create new location.
        """
        data = api.payload
        controller = LocationController()

        current_user, _ = current_app.get_logged_user(request)
        user_id = current_user.id

        return controller.create(data=data, user_id=user_id)


@api.route('/all/location')
class LocationAllList(Resource):
    @token_required
    @api.expect(get_parser)
    @api.response(code=200, model=location_response, description='Model for location response.')
    def get(self):
        """
        Get all location.
        """
        args = get_parser.parse_args()
        controller = LocationController()
        return controller.get(args=args)


@api.route('/all/location/<int:id>')
class LocationAll(Resource):
    @token_required
    @api.response(code=200, model=location_response, description='Model for location response.')
    def get(self, id):
        """
        Get location by its ID.
        """
        controller = LocationController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(location_request)
    @api.response(code=200, model=location_response, description='Model for location response.')
    def patch(self, id):
        """Update existing location by its ID.
        """

        data = api.payload
        controller = LocationController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        """Delete location by its ID.
        """
        controller = LocationController()
        return controller.delete(object_id=id)
