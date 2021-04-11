#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class PollSelectDto(Dto):
    name = 'poll_select'
    api = Namespace(name, description="Poll Select operations")

    model_user = api.model('user', {
        'id': fields.Integer(readonly=True, description='The ID of the user'),
        'profile_pic_url': fields.String(description='The profile url of the user'),
        'display_name': fields.String(description='The display name url of the user'),
    })

    model_request = api.model('poll_select_request', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the poll user select'),
        'user': fields.Nested(model_user, description='The detail of user selecting'),
        'poll_id': fields.Integer(description='The ID of the poll'),
        'poll_select_id': fields.Integer(description='The ID of the poll select'),
    })

    model_response = api.model('poll_select_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the poll'),
        'poll_id': fields.Integer(description='The ID of the poll'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
        "created_by_user": fields.Nested(model_user, description='The detail of user creating'),
        'content': fields.String(default=None, description='The content of the poll select'),
        'poll_user_selects': fields.Nested(model_request, description='List all users selecting'),
    })

    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('poll_id', type=str, required=False, help='The ID of the current poll')

