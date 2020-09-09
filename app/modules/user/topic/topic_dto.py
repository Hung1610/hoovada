#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicDto(Dto):
    name = 'user_topic'
    api = Namespace(name, description="User topic operations")

    model_topic = api.model('topic_for_user', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    topic_user = api.model('user_topic_user', {
        'id': fields.Integer(readonly=True, description='The user ID'),
        'display_name': fields.String(required=True, description='The display name of the user'),
        'profile_pic_url': fields.String(required=True, description='The avatar address of the user')
    })

    model_request = api.model('user_topic_request', {
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'topic_id': fields.Integer(description='The ID of the parent topic'),
        'description': fields.String(required=True, description='The content of the topic'),
    })

    model_response = api.model('user_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the topic'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic': fields.Nested(model_topic, description='The information of the user'),
        'topic_id': fields.Integer(description='The ID of the parent topic'),
        'topic': fields.Nested(model_topic, description='The information of the user'),
        'description': fields.String(required=True, description='The content of the topic'),
        'user_id': fields.Integer(required=True, description='The ID of the user'),
        'user': fields.Nested(topic_user, description='The information of the user'),
        'updated_date': fields.DateTime(description='The date topic was updated'),
        'created_date': fields.DateTime(required=True, description='The date topic was created')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('fixed_topic_id', type=int, required=False, help='Search topic by fixed_topic_id')
    model_get_parser.add_argument('topic_id', type=int, required=False, help='Search topic by topic_id')

