#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace, reqparse

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFollowDto(Dto):
    name = 'user_follow'
    api = Namespace(name, description="User follow operations")

    model_topic_user_follow = api.model('topic_user_follow', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_follow_user = api.model('follow_user', {
        'title': fields.String(description='The title of the user'),
        'user_id': fields.Integer(description='The user information'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'topics': fields.List(fields.Nested(model_topic_user_follow), description='The list of topics')
    })

    model_request = api.model('follow_user_request', {
    })

    model_response = api.model('follow_user_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'follower_id': fields.Integer(required=True, description='The user ID who friendd'),
        'follower':fields.Nested(model_follow_user, description='The information of the following user'),
        'followee_id': fields.Integer(required=False, description='The user ID who has been followed'),
        'followee':fields.Nested(model_follow_user, description='The information of the followed user'),
        'is_approved': fields.Boolean(default=False, description='This follow request is approved or not'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    top_user_followee_args_parser = reqparse.RequestParser()
    top_user_followee_args_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
    top_user_followee_args_parser.add_argument('topic', type=int, action='append', required=True, help='Relevant topics IDs')

    top_user_followee_response = api.model('top_user_followee_response', {
        'user': fields.Nested(model_topic_user_follow, description='The user information'),
        'total_score': fields.Integer(default=0, description='The total reputation score of user for relevant topics'),
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('follower_id', type=str, required=False, help='Search friends by follower_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all follow request by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all follow request by finish voting date.')
