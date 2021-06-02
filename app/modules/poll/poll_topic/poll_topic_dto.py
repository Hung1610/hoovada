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


class PollTopicDto(Dto):
    name = 'poll_topic'
    api = Namespace(name, description="Poll Topic operations")

    model_poll = api.model('poll', {
        'id': fields.Integer(readonly=True, description='The ID of the poll'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
    })


    model_topic = api.model('topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic'),
        'is_fixed': fields.Boolean(description='Is a fixed topic'),
    })


    model_response = api.model('poll_topic_response', {
        'id': fields.Integer(readonly=True, description='The ID of the poll topic'),
        'poll_id': fields.Integer(description='The ID of the poll'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
        'poll': fields.Nested(model_poll, description='Detail of current poll'),
        'topic': fields.Nested(model_topic, description='List topics of the current poll')
    })

    model_request = api.model('poll_topic_request', {
        'topic_id': fields.String(default=None, description='The ID of the topic'),
    })
    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('topic_id', type=str, required=False, help='The ID of the choosen topic')
