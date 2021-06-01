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


class CareerDto(Dto):
    name = 'career'
    api = Namespace(name, description="Career operations")

    model_career_request = api.model('career_request', {
        'title': fields.String(description='The title of the career'),
        'description': fields.String(description='The description of the career'),
        'requirements': fields.String(description='The requirements of the career'),
        'location': fields.String(description='The location of the career'),
        'contact': fields.String(description='The contact of the career'),
        'salary_from': fields.Integer(description='The amount of salary, starting from'),
        'salary_to': fields.Integer(description='The amount of salary, end range'),
        'expire_date': fields.DateTime(description='The expiry date of the career opportunity'),
    })

    model_career_response = api.model('career_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the career'),
        'slug': fields.String(description='The slug of the career'),
        'description': fields.String(description='The description of the career'),
        'requirements': fields.String(description='The requirements of the career'),
        'location': fields.String(description='The location of the career'),
        'contact': fields.String(description='The contact of the career'),
        'expire_date': fields.DateTime(description='The expiry date of the career opportunity'),
        'salary_from': fields.Integer(description='The amount of salary, starting from'),
        'salary_to': fields.Integer(description='The amount of salary, end range'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
    })

    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('title', type=str, required=False, help='Search career by its title')
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search all careers created by user.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date' ", type=str,
                            choices=('created_date', 'updated_date'), action='append',)
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date' ", type=str,
                            choices=('created_date', 'updated_date'), action='append',)
