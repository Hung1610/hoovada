#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from werkzeug.datastructures import FileStorage

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
        'color_code': fields.String(description='The color code for topic'),
        'description': fields.String(description='Description about topic'),
        'is_nsfw': fields.Boolean(default=False, description='This topic is nsfw or not'),
    })

    # define the model for response
    model_topic_response = api.model('topic_response', {
        'id': fields.Integer(requried=False, readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the question'),
        'name': fields.String(description='The name of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'file_url': fields.String(description='The file url for topic'),
        'user_id': fields.Integer(description='The user ID'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'user_count': fields.Integer(description='The amount of users who interest this topic'),
        'answer_count': fields.Integer(description='The amount of answers in this topic'),
        'parent_id': fields.Integer(description='The ID of parent (fixed) topic'),
        'is_fixed': fields.Boolean(default=False, description='This topic is fixed or not'),
        'created_date': fields.DateTime(description='The date topic was created'),
        'description': fields.String(description='Description about topic'),
        'is_nsfw': fields.Boolean(default=False, description='This topic is nsfw or not'),
        'children': fields.List(fields.Nested(model_sub_topic), description='List of sub-topic belong to this topic'),
    })

    topic_endorse_user_request = api.model('topic_endorse_user_request', {
        'user_id': fields.Integer(required=True, description='User id to endorse'),
    })

    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files',
                        type=FileStorage, required=True)

    @classmethod
    def get_endorsed_users_parser(cls):
        get_endorsed_users_parser = cls.paginated_request_parser.copy()
        return get_endorsed_users_parser