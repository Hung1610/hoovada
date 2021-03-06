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
    name = 'article_favorite'
    api = Namespace(name, description="Article favorite operations")

    model_topic_article_favorite = api.model('topic_article_favorite', {
        'id': fields.Integer(readonly=True, description='The ID of the topic'),
        'name': fields.String(description='The name of the topic')
    })

    model_favorite_article = api.model('favorite_article', {
        'title': fields.String(description='The title of the article'),
        'user_id': fields.Integer(description='The user information'),
        'topics': fields.List(fields.Nested(model_topic_article_favorite), description='The list of topics')
    })

    model_request = api.model('favorite_article_request', {
    })

    model_response = api.model('favorite_article_response', {
        'id': fields.Integer(required=False, readonly=True, description='The ID of the record'),
        'user_id': fields.Integer(required=True, description='The user ID who favorited'),
        'article_id': fields.Integer(required=False, description='The user ID who has been favorited'),
        'article':fields.Nested(model_favorite_article, description='The information of the article'),
        'created_date': fields.DateTime(required=False, description='The created date'),
        'updated_date': fields.DateTime(required=False, description='The updated date'),
        'entity_type': fields.String(default='user', description='Type of entity, default is "user"'),
        'organization_id': fields.String(description='The ID of organization. Must be specified when entity_type is organization')
    })

    model_get_parser = reqparse.RequestParser()
    model_get_parser.add_argument('user_id', type=str, required=False, help='Search favorites by user_id')
    model_get_parser.add_argument('from_date', type=str, required=False, help='Search all favorites by start voting date.')
    model_get_parser.add_argument('to_date', type=str, required=False, help='Search all favorites by finish voting date.')
    model_get_parser.add_argument('favorited_user_id', type=str, required=False, help='Search favorites by user owner of the article')
