#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Namespace, fields, reqparse

# own modules
from app.modules.common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleDto(Dto):
    name = 'article'
    api = Namespace(name)

    model_topic = api.model('topic_for_article', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_article_user = api.model('article_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False)
    })

    model_article_request = api.model('article_request', {
        'title': fields.String(description='The title of the article'),
        'user_id': fields.Integer(description='The user ID'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'html': fields.String(description='The content of the article'),
        'user_hidden': fields.Boolean(default=False,
                                      description='The article wss created by user but the user want to be hidden'),
        'topic_ids': fields.List(fields.Integer, description='The list of topics')
    })

    model_article_response = api.model('article_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the article'),
        'user': fields.Nested(model_article_user, description='The user information'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic_name': fields.String(description='The name of the parent (fixed) topic'),
        'html': fields.String(description='The content of the article'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of article views'),
        'last_activity': fields.DateTime(description='The last time this article was updated.'),
        'user_hidden': fields.Boolean(default=False,
                                      description='The article wss created by user but the user want to be hidden'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('title', type=str, required=False, \
        help='Search article by its title')
    model_get_parser.add_argument('fixed_topic_id', type=str, required=False, \
        help='Search all articles related to fixed-topic.')
    model_get_parser.add_argument('topic_name', type=str, required=False, \
        help='Search all articles related to topic.')
    model_get_parser.add_argument('from_date', type=str, required=False, \
        help='Search articles created later that this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, \
        help='Search articles created before this data.')
    model_get_parser.add_argument('anonymous', type=str, required=False, \
        help='Search articles created by Anonymous.')
