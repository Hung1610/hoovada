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


class PostDto(Dto):
    name = 'post'
    api = Namespace(name, description="Post operations")

    model_topic = api.model('topic_for_post', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_post_user = api.model('post_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False)
    })

    model_post_request = api.model('post_request', {
        'title': fields.String(description='The title of the post'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'html': fields.String(description='The content of the post'),
        'topic_ids': fields.List(fields.Integer, description='The list of topics'),
        'scheduled_date': fields.DateTime(description='The scheduled date'),
        'allow_favorite': fields.Boolean(default=False, description='The post allows favoriting or not'),
        'is_draft': fields.Boolean(default=False, description='The post is a draft or not'),
        'is_deleted': fields.Boolean(default=False, description='The post is soft deleted or not'),
    })

    model_post_response = api.model('post_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the post'),
        'slug': fields.String(description='The slug of the post'),
        'user': fields.Nested(model_post_user, description='The user information'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic': fields.Nested(model_topic, description='The parent (fixed) topic'),
        'html': fields.String(description='The content of the post'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of post views'),
        'last_activity': fields.DateTime(description='The last time this post was updated.'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'allow_favorite': fields.Boolean(default=False, description='The post allows favoriting or not'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'is_deleted': fields.Boolean(default=False, description='The post is soft deleted or not'),
        'file_url': fields.String(description='The file url'),
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('title', type=str, required=False, help='Search post by its title')
    model_get_parser.add_argument('fixed_topic_id', type=int, required=False, help='Search all posts related to fixed-topic.')
    model_get_parser.add_argument('topic_id', type=int, required=False, action='append', help='Search all posts related to topic.')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search posts created later than this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search posts created before this data.')
    model_get_parser.add_argument('draft', type=bool, required=False, help='Search posts that are drafts.')
    model_get_parser.add_argument('is_deleted', type=bool, required=False, help='Search posts that are deleted.')
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search all posts created by user.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count'), action='append',
                        )
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count'), action='append',
                        )

    get_similar_posts_parser = reqparse.RequestParser()
    get_similar_posts_parser.add_argument('title', type=str, required=False, help='Title by which to get similar questions')
    get_similar_posts_parser.add_argument('fixed_topic_id', type=int, required=False, help='fixed_topic_id by which to get similar questions')
    get_similar_posts_parser.add_argument('topic_id', type=int, required=False, action='append', help='topic_id by which to get similar questions')
    get_similar_posts_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')