#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class EmploymentDto(Dto):
    name = 'user_employment'
    api = Namespace(name, description="User employment operations")

    model_request = api.model('user_employment_request', {
        'user_id': fields.Integer(required=True, description='The user ID'),
        'position': fields.String(required=True, description='The position'),
        'company': fields.String(required=True, description='The company'),
        'start_year': fields.Integer(description='The start year'),
        'end_year': fields.Integer(description='The end year'),
        'is_current': fields.Integer(description='The currently work'),
        'is_visible': fields.Boolean(default=False, description='Display the user employment or not')
    })


    model_response = api.model('user_employment_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'position': fields.String(required=True, description='The position'),
        'company': fields.String(required=True, description='The company'),
        'start_year': fields.Integer(description='The start year'),
        'end_year': fields.Integer(description='The end year'),
        'is_current': fields.Integer(description='The currently work'),
        'created_date':fields.DateTime(description='The date user_employment record was created.'),
        'is_visible': fields.Boolean(default=False, description='Display the user employment or not')
    })

    parser = reqparse.RequestParser()
    parser.add_argument('is_current', type=int, required=False, help='Is current employment')
