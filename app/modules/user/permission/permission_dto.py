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


class PermissionDto(Dto):
    name = 'permission'
    api = Namespace(name, description='permission related operations')
    model_request = api.model('permission_request', {
        'permission_name': fields.String(required=True, default=''),
        'description': fields.String(required=False, default=''),
    })

    model_response = api.model('permission_response', {
        'id': fields.Integer(readonly=True),
        'permission_name': fields.String(required=False),
        'description': fields.String(required=False),
    })
