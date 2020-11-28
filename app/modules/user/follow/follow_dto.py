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


class UserFollowDto(Dto):
    name = 'user_follow'
    api = Namespace(name, description="User follow operations")

    model_follow_user = api.model('follow_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),

        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_request = api.model('follow_user_request', {
    })

    model_response = api.model('follow_user_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'follower_id': fields.Integer(required=True, description='The user ID who friendd'),
        'follower':fields.Nested(model_follow_user, description='The information of the following user'),
        'followed_id': fields.Integer(required=False, description='The user ID who has been followed'),
        'followed':fields.Nested(model_follow_user, description='The information of the followed user'),
        'is_approved': fields.Boolean(default=False, description='This follow request is approved or not'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    top_user_followee_args_parser = reqparse.RequestParser()
    top_user_followee_args_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
    top_user_followee_args_parser.add_argument('topic', type=int, action='append', required=True, help='Relevant topics IDs')

    top_user_followee_response = api.model('top_user_followee_response', {
        'user': fields.Nested(model_follow_user, description='The user information'),
        'total_score': fields.Integer(default=0, description='The total reputation score of user for relevant topics'),
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('follower_id', type=str, required=False, help='Search friends by follower_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all follow request by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all follow request by finish voting date.')
