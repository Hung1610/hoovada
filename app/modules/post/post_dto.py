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


class PostDto(Dto):
    name = 'post'
    api = Namespace(name, description="Post operations")

    model_post_user = api.model('post_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False),
        'profile_views': fields.Integer(default=False, description='User view count'),
        'is_facebook_linked': fields.Boolean(default=False, description='The user is facebook social linked or not'),
        'is_google_linked': fields.Boolean(default=False, description='The user is google social linked or not'),
        'is_approved_friend': fields.Boolean(default=False, description='The user is approved friend or not'),
        'is_friended_by_me': fields.Boolean(default=False, description='The user is befriended or not'),
        'is_followed_by_me': fields.Boolean(default=False, description='The user is followed or not'),
        'verified_document': fields.Boolean(default=False, description='The user document is verified or not'),
    })

    model_post_request = api.model('post_request', {
        'html': fields.String(description='The content of the post'),
        'is_draft': fields.Boolean(default=False, description='The post is a draft or not'),
        'is_deleted': fields.Boolean(default=False, description='The post is soft deleted or not'),

        'allow_comments': fields.Boolean(default=True, description='Allow comment or not'),
        'allow_favorite': fields.Boolean(default=True, description='Allow favorite or not'),
    })

    model_post_response = api.model('post_response', {
        'id': fields.Integer(readonly=True, description=''),
        'user': fields.Nested(model_post_user, description='The user information'),
        'html': fields.String(description='The content of the post'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of post views'),
        'last_activity': fields.DateTime(description='The last time this post was updated.'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'is_deleted': fields.Boolean(default=False, description='The post is soft deleted or not'),
        'file_url': fields.String(description='The file url'),
        'is_seen_by_me': fields.Boolean(default=False, description='The user is befriended or not'),

        'allow_comments': fields.Boolean(default=True, description='Allow comment or not'),
        'allow_favorite': fields.Boolean(default=True, description='Allow favorite or not'),
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search posts created later than this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search posts created before this data.')
    model_get_parser.add_argument('draft', type=inputs.boolean, required=False, help='Search posts that are drafts.')
    model_get_parser.add_argument('is_deleted', type=inputs.boolean, required=False, help='Search posts that are deleted.')
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search all posts created by user.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'comment_count'", type=str, choices=('created_date', 'updated_date', 'comment_count'), action='append',)
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'comment_count'", type=str, choices=('created_date', 'updated_date', 'comment_count'), action='append',)
