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


class PollUserSelectDto(Dto):
    name = 'poll_user_select'
    api = Namespace(name, description="Poll User Select operations")

    model_user = api.model('user', {
        'id': fields.Integer(readonly=True, description='The ID of the user'),
        'profile_pic_url': fields.String(description='The profile url of the user'),
        'display_name': fields.String(description='The display name url of the user'),
    })

    model_response = api.model('poll_user_select_response', {
        'id': fields.Integer(readonly=True, description='The ID of the poll topic'),
        'poll_select_id': fields.Integer(description='The ID of the poll select'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
        'user': fields.Nested(model_user, description='Detail of current poll'),
    })

    model_request = api.model('poll_user_select_request', {
        'poll_select_id': fields.Integer(description='The ID of the poll select'),
    })

    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('poll_select_id', type=str, required=False, help='The ID of the choosen poll select')
