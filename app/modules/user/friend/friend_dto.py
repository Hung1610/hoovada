#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import inputs
from flask_restx import Namespace, fields, reqparse

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class UserFriendDto(Dto):
    name = 'user_friend'
    api = Namespace(name, description="User friend operations")

    model_friend_user = api.model('friend_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),
        
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),

        'is_endorsed_by_me': fields.Boolean(default=False, description='The user is endorsed or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
    })

    model_request = api.model('friend_user_request', {
    })

    model_response = api.model('friend_user_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'adaptive_friend_id': fields.Integer(required=False, description='The user ID who has been friendd'),
        'adaptive_friend':fields.Nested(model_friend_user, description='The information of the friended user'),
        'is_approved': fields.Boolean(default=False, description='This friend request is approved or not'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    top_user_friend_args_parser = reqparse.RequestParser()
    top_user_friend_args_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')
    top_user_friend_args_parser.add_argument('topic', type=int, action='append', required=True, help='Relevant topics IDs')

    top_user_friend_response = api.model('top_user_friend_response', {
        'user': fields.Nested(model_friend_user, description='The user information'),
        'total_score': fields.Integer(default=0, description='The total reputation score of user for relevant topics'),
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all friends by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all friends by finish voting date.')
    model_get_parser.add_argument('is_approved', type=inputs.boolean, required=False, help='Get all approved friends in database.')
    model_get_parser.add_argument('friend_id', type=int, required=False, help='Search all friends by requested by user id.')
    model_get_parser.add_argument('friended_id', type=int, required=False, help='Search all friends by requested to user id.')
