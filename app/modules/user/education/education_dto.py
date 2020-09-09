#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class EducationDto(Dto):
    name = 'user_education'
    api = Namespace(name, description="User education operations")

    education_user = api.model('user_education_user', {
        'id': fields.Integer(readonly=True, description='The user ID'),
        'display_name': fields.String(required=True, description='The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('user_education_request', {
        'school': fields.String(required=True, description='The content of the education'),
        'primary_major': fields.String(required=True, description='The content of the education'),
        'secondary_major': fields.String(required=False, description='The content of the education'),
        'is_current': fields.Boolean(default=False, description='The education is current or not'),
        'start_year': fields.Integer(required=False, description='The ID of the user'),
        'end_year': fields.Integer(required=False, description='The ID of the user'),
    })

    model_response = api.model('user_education_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the education'),
        'school': fields.String(required=True, description='The content of the education'),
        'primary_major': fields.String(required=True, description='The content of the education'),
        'secondary_major': fields.String(required=False, description='The content of the education'),
        'is_current': fields.Boolean(default=False, description='The education is current or not'),
        'start_year': fields.Integer(required=False, description='The ID of the user'),
        'end_year': fields.Integer(required=False, description='The ID of the user'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(education_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date education was updated'),
        'created_date': fields.DateTime(required=True, description='The date education was created')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('school', type=str, required=False, help='Search education by school name')
    model_get_parser.add_argument('primary_major', type=int, required=False, help='Search all education related to primary_major.')
    model_get_parser.add_argument('secondary_major', type=int, required=False, action='append', help='Search all education related to secondary_major.')

