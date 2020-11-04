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


class TopicFollowDto(Dto):
    name = 'topic_follow'
    api = Namespace(name, description="Topic follow operations")

    model_topic_topic_follow = api.model('topic_topic_follow', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_follow_topic = api.model('follow_topic', {
        'title': fields.String(description='The title of the topic'),
        'user_id': fields.Integer(description='The user information'),
        'topics': fields.List(fields.Nested(model_topic_topic_follow), description='The list of topics')
    })

    model_request = api.model('follow_topic_request', {
    })

    model_response = api.model('follow_topic_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who followd'),
        'topic_id': fields.Integer(required=False, description='The user ID who has been followd'),
        'topic':fields.Nested(model_follow_topic, description='The information of the topic'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search follows by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all follows by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all follows by finish voting date.')
    model_get_parser.add_argument('followed_user_id', type=str, required=False, help='Search follows by user owner of the topic')
