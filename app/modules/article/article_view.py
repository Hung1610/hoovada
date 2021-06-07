#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.article.article_controller import ArticleController
from app.modules.article.article_dto import ArticleDto
from common.cache import cache
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleDto.api

# request model
MODEL_ARTICLE_REQUEST = ArticleDto.model_article_request
MODEL_GET_PARSER = ArticleDto.model_get_parser
GET_SIMILAR_ARTICLES_PARSER = ArticleDto.get_similar_articles_parser

# response model
MODEL_ARTICLE_RESPONSE = ArticleDto.model_article_response
MODEL_ARTICLE_CREATE_UPDATE_RESPONSE = ArticleDto.model_article_create_update_response


@api.route('')
class ArticleList(Resource):
    @api.response(code=200, model=MODEL_ARTICLE_RESPONSE, description='Model for article response.')
    @api.expect(MODEL_GET_PARSER)
    @cache.cached(query_string=True)
    def get(self):
        """Get all articles that satisfy conditions"""

        args = MODEL_GET_PARSER.parse_args()
        controller = ArticleController()
        return controller.get(args=args)


    @token_required
    @api.expect(MODEL_ARTICLE_REQUEST)
    @api.response(code=200, model=MODEL_ARTICLE_CREATE_UPDATE_RESPONSE, description='Model for article response.')
    def post(self):
        """Create new article"""

        data = api.payload
        controller = ArticleController()
        return controller.create(data=data)


@api.deprecated
@api.route('/all/count')
@api.expect(MODEL_GET_PARSER)
class ArticleListCount(Resource):
    def get(self):
        """Count number of articles that satisfy conditions"""

        args = MODEL_GET_PARSER.parse_args()
        controller = ArticleController()
        return controller.get_count(args=args)


def get_article_key_prefix():
    return '{}{}'.format('get.article', request.view_args['id_or_slug'])

@api.route('/<string:id_or_slug>')
class Article(Resource):
    @api.response(code=200, model=MODEL_ARTICLE_RESPONSE, description='Model for article response.')
    @cache.cached(key_prefix=get_article_key_prefix)
    def get(self, id_or_slug):
        """Get an article by article id or slug"""

        controller = ArticleController()
        return controller.get_by_id(object_id=id_or_slug)

    @token_required
    @api.expect(MODEL_ARTICLE_REQUEST)
    @api.response(code=200, model=MODEL_ARTICLE_CREATE_UPDATE_RESPONSE, description='Model for article response.')
    def patch(self, id_or_slug):
        """Update existing article by article Id or slug"""

        data = api.payload
        controller = ArticleController()
        result = controller.update(object_id=id_or_slug, data=data)
        cache.clear_cache(get_article_key_prefix())
        return result


    @token_required
    def delete(self, id_or_slug):
        """ Delete the article by article Id or slug"""

        controller = ArticleController()
        result = controller.delete(object_id=id_or_slug)
        cache.clear_cache(get_article_key_prefix())
        return result


@api.route('/similar')
class ArticleSimilar(Resource):
    @api.expect(GET_SIMILAR_ARTICLES_PARSER)
    @api.response(code=200, model=MODEL_ARTICLE_RESPONSE, description='Model for article response.')
    def get(self):
        """ Get similar articles"""
        
        args = GET_SIMILAR_ARTICLES_PARSER.parse_args()
        controller = ArticleController()
        return controller.get_similar(args=args)
