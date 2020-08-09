#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.article.article_dto import ArticleDto
from app.modules.article.article_controller import ArticleController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleDto.api
_article_dto_request = ArticleDto.model_article_request
_article_dto_response = ArticleDto.model_article_response
_article_get_params = ArticleDto.model_get_parser

@api.route('')
class ArticleList(Resource):
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    @api.expect(_article_get_params)
    def get(self):
        """
        Get all articles that satisfy conditions.
        ---------------------
        :param `title`: The name of the topics to search

        :param `fixed_topic_id`: Search all articles by fixed topic ID.

        :param `topic_name`: Search all articles by topic ID.

        :param `from_date`: Search articles created after this date.

        :param `to_date`: Search articles created before this date.

        :param `anonymous`: Search articles created by anonymous.

        :return: List of articles satisfy search condition.
        """
        args = _article_get_params.parse_args()
        controller = ArticleController()
        return controller.get(args=args)

    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def post(self):
        '''
        Create new article and save to database.

        :return: The article if success and None vice versa.
        '''
        data = api.payload
        controller = ArticleController()
        return controller.create(data=data)


@api.route('/<int:id>')
class Article(Resource):
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def get(self, id):
        '''
        Get specific article by its ID.

        :param id: The ID of the article to get.

        :return: The article if success and None vice versa.
        '''
        controller = ArticleController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def put(self, id):
        '''
        Update existing article by its ID.

        :param id: The ID of the article.

        :return:
        '''
        data = api.payload
        controller = ArticleController()
        return controller.update(object_id=id, data=data)

    @token_required
    def delete(self, id):
        '''
        Delete the article by its ID.

        :param id: The ID of the article.

        :return:
        '''
        controller = ArticleController()
        return controller.delete(object_id=id)