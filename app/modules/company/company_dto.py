#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from datetime import datetime
from flask_restx import inputs, Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class CompanyDto(Dto):
    name = 'company'
    api = Namespace(name, description="Company operations")

    user = api.model('model_user',{
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

    model_company_response = api.model('company_response', {
        'id': fields.Integer(readonly=True, description='The ID of the company'),
        'display_name': fields.String(description='The display name of the company'),
        'description': fields.String(description='The description of the company'),
        'email': fields.String(description='The email of the company'),
        'website_url': fields.String(description='The website url of the company'),
        'status': fields.String(description='The current status of the company'),
        'phone_number': fields.String(description='The phone number of the company'),
        'logo_url': fields.String(description='The logo url of the company'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'user_id': fields.Integer(description='The ID of user owner of the company'),
        'user': fields.Nested(user, description='The user information'),
        'user_count': fields.Integer(description='Number of users joined the company'),
        'article_count': fields.Integer(description='Number of articled published by the company'),
        'is_joined_by_me': fields.Boolean(description='Is joined in the company by me'),
    })

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('display_name', type=str, required=False, help='The display name of the company')
    post_request_parser.add_argument('email', type=str, required=False, help='The email of the company')
    post_request_parser.add_argument('phone_number', type=str, required=False, help='The phone number of the company')
    post_request_parser.add_argument('description', type=str, required=False, help='The description of the company')
    post_request_parser.add_argument('website_url', type=str, required=False, help='The website url of the company')
    post_request_parser.add_argument('logo_url', type=str, required=False, help='The logo url of the company')

    get_list_request_parser = Dto.paginated_request_parser.copy()
    get_list_request_parser.add_argument('display_name', type=str, required=False, help='The display name of the company')
    get_list_request_parser.add_argument('email', type=str, required=False, help='The email of the company')
    get_list_request_parser.add_argument('phone_number', type=str, required=False, help='The phone number of the company')

    update_status_request_parser = reqparse.RequestParser()
    update_status_request_parser.add_argument('status',type=str, required=False, help='The status of the company. Must be one of submitted, approved, rejected, deactivated')
