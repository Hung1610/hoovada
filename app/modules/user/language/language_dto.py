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
    name = 'user_language'
    api = Namespace(name, description="User language operations")

    model_language = api.model('language_for_user', {
        'id': fields.Integer(readonly=True, description='The ID of the language'),
        'name': fields.String(description='The name of the language'),
        'description': fields.String(description='Description about language')
    })

    language_user = api.model('user_language_user', {
        'id': fields.Integer(readonly=True, description='The user ID'),
        'display_name': fields.String(required=True, description='The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('user_language_request', {
        'language_id': fields.Integer(description='The ID of the parent language'),
        'level': fields.String(required=True, description='The level of proficiency of the user for the language'),
    })

    model_response = api.model('user_language_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the language'),
        'language_id': fields.Integer(description='The ID of the parent language'),
        'language': fields.Nested(model_language, description='The information of the user'),
        'level': fields.String(required=True, description='The level of proficiency of the user for the language'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(language_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date language was updated'),
        'created_date': fields.DateTime(required=True, description='The date language was created')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('language_id', type=int, required=False, help='Search language by language_id')

