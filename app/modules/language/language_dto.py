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

class LanguageDto(Dto):
    name = 'language'
    api = Namespace(name, description="Language operations")

    model_request = api.model('language_request', {
        'code': fields.String(required=True, description='The content of the language'),
        'name': fields.String(default=True, description='The language name'),
        'description': fields.Integer(required=False, description='The description'),
    })

    model_response = api.model('language_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the language'),
        'code': fields.String(required=True, description='The code of the language'),
        'name': fields.String(default=True, description='The language name'),
        'description': fields.Integer(required=False, description='The description'),
        'created_date': fields.DateTime(required=True, description='The date language was created')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('code', type=str, required=False, help='Search language by code')
    model_get_parser.add_argument('name', type=str, required=False, help='Search language by name')
