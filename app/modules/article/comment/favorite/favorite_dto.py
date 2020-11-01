#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import fields, Namespace, reqparse 

# own modules
from common.dto import Dto

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


class ArticleCommentFavoriteDto(Dto):
    name = 'article_comment_favorite'
    api = Namespace(name, description="ArticleComment-Favorite operations")

    model_topic_article_comment_favorite = api.model('topic_article_comment_favorite', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_favorite_article_comment = api.model('favorite_article_comment', {
        'title': fields.String(description='The title of the article_comment'),
        'user_id': fields.Integer(description='The user information'),
        'topics': fields.List(fields.Nested(model_topic_article_comment_favorite), description='The list of topics')
    })

    model_request = api.model('favorite_article_comment_request', {
    })

    model_response = api.model('favorite_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who favorited'),
        'favorited_user_id': fields.Integer(required=False, description='The user ID who has been favorited'),
        'article_comment_id': fields.Integer(required=False, description='The article_comment ID which has been favorited'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search favorites by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all favorites by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all favorites by finish voting date.')
    model_get_parser.add_argument('favorited_user_id', type=str, required=False, help='Search favorites by user owner of the article_comment')