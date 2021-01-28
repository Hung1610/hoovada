#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from werkzeug.datastructures import FileStorage

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields

# own modules
from common.dto import Dto

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
        'profile_pic_url': fields.String(required=False),
        'endorsed_count': fields.Integer(required=False),
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed by me or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is followed by me or not'),
        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed by current user or not'),
        'profile_views': fields.Integer(default=False, description='User view count'),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
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
        'color_code': fields.String(description='The color code for topic'),
        'description': fields.String(description='Description about topic'),
        'is_nsfw': fields.Boolean(default=False, description='This topic is nsfw or not'),
        'allow_follow': fields.Boolean(default=False, description='This topic allows following or not'),
    })

    model_parent_topic = api.model('parent_topic', {
        'id': fields.Integer(readonly=True),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about the topic'),
        'color_code': fields.String(description='The color code for topic'),
    })

    # define the model for response
    model_topic_response = api.model('topic_response', {
        'id': fields.Integer(requried=False, readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the question'),
        'name': fields.String(description='The name of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'file_url': fields.String(description='The file url for topic'),
        'user_id': fields.Integer(description='The user ID'),
        'parent_id': fields.Integer(description='The ID of parent (fixed) topic'),
        'is_fixed': fields.Boolean(default=False, description='This topic is fixed or not'),
        'created_date': fields.DateTime(description='The date topic was created'),
        'description': fields.String(description='Description about topic'),
        'is_nsfw': fields.Boolean(default=False, description='This topic is nsfw or not'),
        'allow_follow': fields.Boolean(default=False, description='This topic allows following or not'),
        'children': fields.List(fields.Nested(model_sub_topic), description='List of sub-topic belong to this topic'),
        'parent': fields.Nested(model_parent_topic, description='The parent (fixed) topic'),
        'article_count': fields.Integer(description='The amount of article belong to this topic'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'endorsers_count': fields.Integer(description='The amount of endorsers belong to this topic'),
        'bookmarkers_count': fields.Integer(description='The amount of bookmarkers belong to this topic'),
        'followers_count': fields.Integer(description='The amount of followers belong to this topic'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'is_followed_by_me': fields.Boolean(default=False, description='The topic is followed by current user or not'),
    })

    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('name', type=str, required=False, help='The name of the topic')
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search topic by user_id (who created topic)')
    model_get_parser.add_argument('parent_id', type=int, required=False, help='Search all sub-topics which belongs to the parent ID.')
    model_get_parser.add_argument('is_fixed', type=inputs.boolean, required=False, help='Get all fixed topics in database.')
    model_get_parser.add_argument('hot', type=inputs.boolean, required=False, help='Search topics that are hot.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )

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