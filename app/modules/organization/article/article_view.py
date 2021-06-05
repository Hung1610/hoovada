#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask import request
from flask_restx import Resource, reqparse

# own modules
from app.modules.organization.article.article_controller import ArticleController
from app.modules.organization.article.article_dto import ArticleDto
from common.cache import cache
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleDto.api
_article_dto_request = ArticleDto.model_article_request
_article_dto_response = ArticleDto.model_article_response
_article_get_params = ArticleDto.model_get_parser

@api.route('/<int:organization_id>/article')
class ArticleList(Resource):
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    @api.expect(_article_get_params)
    @cache.cached(query_string=True)
    def get(self, organization_id):
        """Get all articles that satisfy conditions"""

        args = _article_get_params.parse_args()
        controller = ArticleController()
        args['organization_id'] = organization_id
        return controller.get(args=args)


    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def post(self, organization_id):
        """Send an article to organization"""

        data = api.payload
        data['organization_id'] = organization_id
        controller = ArticleController()
        return controller.create(data=data)


def get_article_key_prefix():
    return '{}{}'.format('get.article', request.view_args['id_or_slug'])

@api.route('/all/article/<string:id_or_slug>/status')
class ArticleStatus(Resource):
    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def patch(self, id_or_slug):
        """Update status of a organization's article"""

        data = api.payload
        controller = ArticleController()
        result = controller.update_status(object_id=id_or_slug, data=data)
        cache.clear_cache(get_article_key_prefix())
        return result

@api.route('/all/article/<string:id_or_slug>')
class Article(Resource):
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def get(self, id_or_slug):
        """Get an article by article id or slug"""

        controller = ArticleController()
        return controller.get_by_id(object_id=id_or_slug)

    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def patch(self, id_or_slug):
        """Update existing article by article Id or slug"""

        data = api.payload
        controller = ArticleController()
        result = controller.update(object_id=id_or_slug, data=data)
        return result


    @token_required
    def delete(self, id_or_slug):
        """ Delete the article by article Id or slug"""

        controller = ArticleController()
        result = controller.delete(object_id=id_or_slug)
        return result