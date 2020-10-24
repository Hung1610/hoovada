#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields

# own modules
from app.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserTopicDto(Dto):
    name = 'user_topic'
    api = Namespace(name, description="User-Topic operations")

    model_request = api.model('user_topic_request', {
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The topic ID')
    })
    model_response = api.model('user_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the user_topic record'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'topic_id': fields.Integer(required=True, description='The topic ID'),
        'created_date':fields.DateTime(description='The date user_topic record was created.')
    })
