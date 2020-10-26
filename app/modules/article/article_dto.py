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


class ArticleDto(Dto):
    name = 'article'
    api = Namespace(name, description="Article operations")

    model_topic = api.model('topic_for_article', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic'),
        'slug': fields.String(description='The slug of the topic'),
        'description': fields.String(description='Description about topic')
    })

    model_article_user = api.model('article_user', {
        'id': fields.Integer(readonly=True),
        'display_name': fields.String(required=False),
        'profile_pic_url': fields.String(required=False)
    })

    model_article_request = api.model('article_request', {
        'title': fields.String(description='The title of the article'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'html': fields.String(description='The content of the article'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting on this article'),
        'topic_ids': fields.List(fields.Integer, description='The list of topics'),
        'scheduled_date': fields.DateTime(description='The scheduled date'),
        'is_draft': fields.Boolean(default=False, description='The article is a draft or not'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
    })

    model_article_response = api.model('article_response', {
        'id': fields.Integer(readonly=True, description=''),
        'title': fields.String(description='The title of the article'),
        'slug': fields.String(description='The slug of the article'),
        'user': fields.Nested(model_article_user, description='The user information'),
        'fixed_topic_id': fields.Integer(description='The ID of the parent (fixed) topic'),
        'fixed_topic': fields.Nested(model_topic, description='The fixed topic'),
        'html': fields.String(description='The content of the article'),
        'allow_voting': fields.Boolean(default=True, description='Allow voting on this article'),
        'created_date': fields.DateTime(description='The created date'),
        'updated_date': fields.DateTime(description='The updated date'),
        'views_count': fields.Integer(default=0, description='The amount of article views'),
        'last_activity': fields.DateTime(description='The last time this article was updated.'),
        'topics': fields.List(fields.Nested(model_topic), description='The list of topics'),
        'upvote_count': fields.Integer(default=0, description='The amount of upvote'),
        'downvote_count': fields.Integer(default=0, description='The amount of downvote'),
        'share_count': fields.Integer(default=0, description='The amount of sharing'),
        'favorite_count': fields.Integer(default=0, description='The amount of favorite'),
        'comment_count': fields.Integer(default=0, description='The amount of comments'),
        'up_vote':fields.Boolean(default=False, description='The value of upvote of current user.'),
        'down_vote':fields.Boolean(default=False, description='The value of downvote of current user'),
        'is_favorited_by_me':fields.Boolean(default=False, description='The favorited status of current user'),
        'is_deleted': fields.Boolean(default=False, description='The article is soft deleted or not'),
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('title', type=str, required=False, help='Search article by its title')
    model_get_parser.add_argument('fixed_topic_id', type=int, required=False, help='Search all articles related to fixed-topic.')
    model_get_parser.add_argument('topic_id', type=int, required=False, action='append', help='Search all articles related to topic.')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search articles created later than this date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search articles created before this data.')
    model_get_parser.add_argument('draft', type=bool, required=False, help='Search articles that are drafts.')
    model_get_parser.add_argument('is_deleted', type=bool, required=False, help='Search articles that are deleted.')
    model_get_parser.add_argument('user_id', type=int, required=False, help='Search all articles created by user.')
    model_get_parser.add_argument('order_by_desc', help="Order by descending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count'), action='append',
                        )
    model_get_parser.add_argument('order_by_asc', help="Order by ascending. Allowed fields: 'created_date', 'updated_date', 'upvote_count', 'comment_count'", type=str,
                            choices=('created_date', 'updated_date', 'upvote_count', 'comment_count'), action='append',
                        )

    get_similar_articles_parser = reqparse.RequestParser()
    get_similar_articles_parser.add_argument('title', type=str, required=False, help='Title by which to get similar questions')
    get_similar_articles_parser.add_argument('fixed_topic_id', type=int, required=False, help='fixed_topic_id by which to get similar questions')
    get_similar_articles_parser.add_argument('topic_id', type=int, required=False, action='append', help='topic_id by which to get similar questions')
    get_similar_articles_parser.add_argument('limit', type=int, default=10, required=True, help='Limit amount to return')