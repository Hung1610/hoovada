#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReputationDto(Dto):
    name = 'reputation'
    api = Namespace(name, description="Reputation operations")

    model_request = api.model('reputation_request', {
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The Topic ID'),
        'score': fields.Float(required=True, description='The Score'),
    })


    model_response = api.model('reputation_response', {
        'id': fields.Integer(required=False, readonly=True, description='The Reputation ID'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The Topic ID'),
        'score': fields.Float(required=True, description='The Score'),
    })


    user_reputation_response = api.model('user_reputation_response', {
        'id': fields.Integer(required=False, readonly=True, description='The user ID'),
        'display_name': fields.String(required=False),
        'first_name': fields.String(required=False),
        'middle_name': fields.String(required=False),
        'last_name': fields.String(required=False),
        'reputation': fields.Nested(model_response, description='The reputation information'),
    })
