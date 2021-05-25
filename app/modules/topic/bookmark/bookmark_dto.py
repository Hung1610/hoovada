#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class TopicBookmarkDto(Dto):
    name = 'topic_bookmark'
    api = Namespace(name, description="Topic bookmark operations")

    model_bookmark_parent_topic = api.model('topic_topic_bookmark', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'article_count': fields.Integer(description='The amount of article belong to this topic'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'endorsers_count': fields.Integer(description='The amount of endorsers belong to this topic'),
        'bookmarkers_count': fields.Integer(description='The amount of bookmarkers belong to this topic'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'is_followed_by_me': fields.Boolean(default=False, description='The topic is followed by current user or not'),
    })

    model_bookmark_topic = api.model('bookmark_topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
        'parent': fields.Nested(model_bookmark_parent_topic, description='The parent (fixed) topic'),
        'article_count': fields.Integer(description='The amount of article belong to this topic'),
        'question_count': fields.Integer(description='The amount of questions belong to this topic'),
        'endorsers_count': fields.Integer(description='The amount of endorsers belong to this topic'),
        'bookmarkers_count': fields.Integer(description='The amount of bookmarkers belong to this topic'),
        'is_bookmarked_by_me':fields.Boolean(default=False, description='The booomarked status of current user'),
        'is_followed_by_me': fields.Boolean(default=False, description='The topic is followed by current user or not'),
    })

    model_request = api.model('bookmark_topic_request', {
    })

    model_response = api.model('bookmark_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who bookmarkd'),
        'topic_id': fields.Integer(required=False, description='The user ID who has been bookmarkd'),
        'topic':fields.Nested(model_bookmark_topic, description='The information of the topic'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_bookmark_multiple_topics_request = api.model('bookmark_multiple_topics_request', {
        'topic_ids': fields.List(fields.Integer, description='The list of topics'),
    })

    model_bookmark_multiple_topics_response = api.model('bookmark_multiple_topics_response', {
    })


    model_get_parser = Dto.paginated_request_parser.copy()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search bookmarks by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all bookmarks by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all bookmarks by finish voting date.')
    model_get_parser.add_argument('bookmarkd_user_id', type=str, required=False, help='Search bookmarks by user owner of the topic')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date'", type=str,
                            choices=('created_date', 'updated_date'), action='append',
                        )
