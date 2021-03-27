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


class FavoriteDto(Dto):
    name = 'post_favorite'
    api = Namespace(name, description="Post favorite operations")

    model_topic_post_favorite = api.model('topic_post_favorite', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_favorite_post = api.model('favorite_post', {
        'title': fields.String(description='The title of the post'),
        'user_id': fields.Integer(description='The user information'),
        'topics': fields.List(fields.Nested(model_topic_post_favorite), description='The list of topics')
    })

    model_request = api.model('favorite_post_request', {
    })

    model_response = api.model('favorite_post_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who favorited'),
        'post_id': fields.Integer(required=False, description='The user ID who has been favorited'),
        'post':fields.Nested(model_favorite_post, description='The information of the post'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search favorites by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all favorites by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all favorites by finish voting date.')
    model_get_parser.add_argument('favorited_user_id', type=str, required=False, help='Search favorites by user owner of the post')
