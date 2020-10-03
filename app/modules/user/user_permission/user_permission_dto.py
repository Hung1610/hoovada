#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from flask_restx import Namespace, fields

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserPermissionDto(Dto):
    name = 'user_permission'
    api = Namespace(name)
    model_request = api.model('user_permission_request', {
        'user_id': fields.String(required=True, description='Account for set permission'),
        'permissions': fields.List(fields.String, required=True, description='Permissions {[{"name": "ANWSER_VOTE", "allow": 1},{"name": "ANWSER_SHARE", "allow": 1}]}'),
    })

    model_response = api.model('user_permission_response', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'permission_name': fields.String(required=False),
        'allow': fields.String(required=False),
    })

    model_response_create = api.model('user_permission_response', {
        'id': fields.Integer(readonly=True),
    })
