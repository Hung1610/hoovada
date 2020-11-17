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

    model_topic_topic_bookmark = api.model('topic_topic_bookmark', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_bookmark_topic = api.model('bookmark_topic', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'name': fields.String(description='The name of the topic'),
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

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search bookmarks by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all bookmarks by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all bookmarks by finish voting date.')
    model_get_parser.add_argument('bookmarkd_user_id', type=str, required=False, help='Search bookmarks by user owner of the topic')
