#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from datetime import datetime
from flask_restx import inputs, Namespace, fields, reqparse

# own modules
from common.dto import Dto
from app.modules.organization.organization_dto import OrganizationDto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class OrganizationUserDto(Dto):
    name = 'organization_user'
    api = Namespace(name, description="OrganizationUser operations")

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

    model_organization_user_response = api.model('organization_user_response', {
        'id': fields.Integer(readonly=True, description='The ID of the organization'),
        'organization_id': fields.Integer(description='The ID of the organization'),
        'organization': fields.Nested(OrganizationDto.model_organization_response, description='The organization information'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'user_id': fields.Integer(description='The ID of the partner'),
        'user': fields.Nested(user, description='The user information'),
        'status': fields.String(description='The current status of the organization user'),
    })

    get_list_request_parser = Dto.paginated_request_parser.copy()
    get_list_request_parser.add_argument('organization_ud', type=str, required=False, help='The ID of the organization')
    get_list_request_parser.add_argument('status', type=str, required=False, help='The status of the organization user')

    update_status_request_parser = reqparse.RequestParser()
    update_status_request_parser.add_argument('status',type=str, required=False, help='The status of the organization. Must be one of submitted, approved, rejected, deactivated')