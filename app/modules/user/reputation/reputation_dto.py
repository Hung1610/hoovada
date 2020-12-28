#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ReputationDto(Dto):
    name = 'user_reputation'
    api = Namespace(name, description="Reputation operations")

    model_topic = api.model('reputation_topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'description': fields.String(description='Description about topic')
    })

    model_request = api.model('reputation_request', {
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The Topic ID'),
        'score': fields.Float(required=True, description='The Score'),
    })

    model_response = api.model('reputation_response', {
        'id': fields.Integer(required=False, readonly=True, description='The Reputation ID'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The Topic ID'),
        'topic': fields.Nested(model_topic, description='The reputation topic'),
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
