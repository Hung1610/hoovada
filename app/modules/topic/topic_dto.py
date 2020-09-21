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

class TopicDto(Dto):
    name = 'topic'
    api = Namespace(name, description="Topic operations")

    model_endorsed_user = api.model('model_endorsed_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False)
    })

    model_sub_topic = api.model('sub_topic', {
        'id': fields.Integer(readonly=True),
        'name': fields.String(description='The name of the topic'),
        'user_id': fields.Integer(description='The user ID'),
        'question_count': fields.Integer(description='The amount of question related to this topic'),
        'user_count': fields.Integer(description='The amount of user followed this topic'),
        'created_date': fields.DateTime(description='The date topic was created'),
        'description': fields.String(description='Description about the topic')
    })

    # define the model for request
    model_topic_request = api.model('topic_request', {
        'name': fields.String(required=True, description='The name of the topic'),
        'parent_id': fields.Integer(required=True, description='The ID of the parent topic'),
        'user_id': fields.Integer(required=True, description='The user ID'),
        'description': fields.String(description='Description about topic')
    })

    # define the model for response
    model_topic_response = api.model('topic_response', {
        'id': fields.Integer(requried=False, readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        # 'count': fields.Integer(description=''),
        'user_id': fields.Integer(description='The user ID'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'user_count': fields.Integer(description='The amount of users who interest this topic'),
        'answer_count': fields.Integer(description='The amount of answers in this topic'),
        'parent_id': fields.Integer(description='The ID of parent (fixed) topic'),
        'is_fixed': fields.Boolean(default=False, description='This topic is fixed or not'),
        'created_date': fields.DateTime(description='The date topic was created'),
        'description': fields.String(description='Description about topic'),
        'sub_topics': fields.List(fields.Nested(model_sub_topic), description='List of sub-topic belong to this topic')
    })

    topic_endorse_user_request = api.model('topic_endorse_user_request', {
        'user_ids': fields.List(fields.String, description='The list of user ids to endorse'),
    })

    @classmethod
    def get_endorsed_users_parser(cls):
        get_endorsed_users_parser = cls.paginated_request_parser.copy()
        return get_endorsed_users_parser