#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from datetime import datetime
from flask_restx import inputs, Namespace, fields, reqparse

# own modules
from common.dto import Dto
from app.modules.company.company_dto import CompanyDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CompanyUserDto(Dto):
    name = 'company_user'
    api = Namespace(name, description="CompanyUser operations")

    user = api.model('model_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),
        'profile_views': fields.Integer(default=False),
        'endorsed_count': fields.Integer(required=False),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),
        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_company_user_response = api.model('company_response', {
        'id': fields.Integer(readonly=True, description='The ID of the company'),
        'company_id': fields.Integer(description='The ID of the company'),
        'company': fields.Nested(CompanyDto.model_company_response, description='The company information'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'user_id': fields.Integer(description='The ID of the partner'),
        'user': fields.Nested(user, description='The user information'),
        'status': fields.String(description='The current status of the company user'),
    })

    get_list_request_parser = Dto.paginated_request_parser.copy()
    get_list_request_parser.add_argument('company_ud', type=str, required=False, help='The ID of the company')
    get_list_request_parser.add_argument('status', type=str, required=False, help='The status of the company user')

    update_status_request_parser = reqparse.RequestParser()
    update_status_request_parser.add_argument('status',type=str, required=False, help='The status of the company. Must be one of submitted, approved, rejected, deactivated')
