#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserBanDto(Dto):
    name = 'user_ban'
    api = Namespace(name, description="User ban operations")

    model_ban_user = api.model('ban_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False)
    })

    model_request = api.model('ban_user_request', {
        'ban_type': fields.Integer(description='1 - EMAIL, 2 - PHONE_NUMBER', required=False),
        'expiry_date': fields.DateTime(required=False, description='The expiry_date')
    })

    model_response = api.model('ban_user_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'ban_by': fields.String(required=True, description='The string to ban by'),
        'ban_type': fields.Integer(description='1 - EMAIL, 2 - PHONE_NUMBER', required=False),
        'user_id': fields.Integer(required=False, description='The user ID who has been band'),
        'user':fields.Nested(model_ban_user, description='The information of the baned user'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'expiry_date': fields.DateTime(required=False, description='The expiry_date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('ban_by', type=str, required=False, help='Search bans by ban_by')
    model_get_parser.add_argument('expiry_date', type=str, required=False, help='Search all bans by expiry_date.')
    model_get_parser.add_argument('created_date', type=str, required=False, help='Search all bans by created_date.')
