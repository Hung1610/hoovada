#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class LocationDto(Dto):
    name = 'user_location'
    api = Namespace(name, description="User location operations")

    location_user = api.model('user_location_user', {
        'id': fields.Integer(readonly=True, description='The user ID'),
        'display_name': fields.String(required=True, description='The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('user_location_request', {
        'location_detail': fields.String(required=True, description='The content of the location'),
        'is_current': fields.Boolean(default=False, description='The location is current or not'),
        'start_year': fields.Integer(required=False, description='The ID of the user'),
        'end_year': fields.Integer(required=False, description='The ID of the user'),
    })

    model_response = api.model('user_location_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the location'),
        'location_detail': fields.String(required=True, description='The content of the location'),
        'is_current': fields.Boolean(default=False, description='The location is current or not'),
        'start_year': fields.Integer(required=False, description='The ID of the user'),
        'end_year': fields.Integer(required=False, description='The ID of the user'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(location_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date location was updated'),
        'created_date': fields.DateTime(required=True, description='The date location was created')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('location_detail', type=str, required=False, help='Search location by location_detail')
    model_get_parser.add_argument('is_current', type=inputs.boolean, required=False, help='Search location by location_detail')

