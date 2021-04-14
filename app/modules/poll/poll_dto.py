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


class PollDto(Dto):
    name = 'poll'
    api = Namespace(name, description="Poll operations")

    model_user = api.model('user', {
        'id': fields.Integer(readonly=True, description='The ID of the user'),
        'profile_pic_url': fields.String(description='The profile url of the user'),
        'display_name': fields.String(description='The display name url of the user'),
    })

    model_topic = api.model('topic_for_poll', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'color_code': fields.String(description='The color code for topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic'),
    })

    model_poll_user_select = api.model('model_poll_user_select', {
        'user': fields.Nested(model_user, description='The detail of owner user'),
    })

    model_poll_select = api.model('poll_select', {
        'content': fields.String(description='The content of selection of a poll'),
        'poll_user_selects': fields.List(fields.Nested(model_poll_user_select), description='The list of users selecting'),
        'created_by_user': fields.Nested(model_user, description='User that select this selection')
    })

    model_response = api.model('poll_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the poll'),
        'created_date': fields.DateTime(default=datetime.utcnow, description='The date poll was created'),
        'updated_date': fields.DateTime(default=datetime.utcnow, description='The date poll was updated'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'own_user': fields.Nested(model_user, description='The detail of owner user'),
        'title': fields.String(default=None, description='The title of the poll'),
        'allow_multiple_user_select': fields.Boolean(description='Allow user to choose multiple selections'),
        'expire_after_seconds': fields.Integer(default=86400, description='The ID of the question'),
        'poll_selects': fields.Nested(model_poll_select, description='List all selections of a poll'),
        'poll_select_count': fields.Integer(description='Total count of selections'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),

        'fixed_topic': fields.Nested(model_topic, description='The name of the parent (fixed) topic'),
    })

    model_request = api.model('poll_request', {
        'title': fields.String(default=None, description='The title of the poll'),
        'allow_multiple_user_select': fields.Boolean(description='Allow user to choose multiple selections'),
        'expire_after_seconds': fields.Integer(default=86400, description='The ID of the question'),
        'poll_selects':fields.List(fields.String(description='The content of poll select'), description='The list of poll selects'),
        'poll_topics':fields.List(fields.Integer(required=False, description='The ID of the topic'), description='The list of poll topics')
    })
    get_parser = Dto.paginated_request_parser.copy()
    get_parser.add_argument('owner_user_id', type=str, required=False, help='ID of owner user. Default value is current user id')
    get_parser.add_argument('from_date', type=str, required=False, help='Search polls created later that this date.')
    get_parser.add_argument('to_date', type=str, required=False, help='Search polls created before this data.')
    get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
    get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
