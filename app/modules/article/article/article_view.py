#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.article.article.article_dto import ArticleDto
from app.modules.article.article.article_controller import ArticleController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleDto.api
model_request = ArticleDto.model_article_request
model_response = ArticleDto.model_article_response

@api.route('')
class ArticleList(Resource):
    @token_required
    # @api.marshal_list_with(article)
    @api.response(code=200, model=model_response, description='Model for article response.')
    def get(self):
        '''
        Get list of articles from database.

        :return: List of articles.
        '''
        controller = ArticleController()
        return controller.get()

    @token_required
    @api.expect(model_request)
    # @api.marshal_with(article)
    @api.response(code=200, model=model_response, description='Model for article response.')
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
    @token_required
    # @api.marshal_with(article)
    # @api.param(name='id', description='The ID of thearticle.')
    @api.response(code=200, model=model_response, description='Model for article response.')
    def get(self, id):
        '''
        Get specific article by its ID.

        :param id: The ID of the article to get from.

        :return: The article if success and None vice versa.
        '''
        controller = ArticleController()
        return controller.get_by_id(object_id=id)

    @token_required
    @api.expect(model_request)
    # @api.marshal_with(article)
    @api.response(code=200, model=model_response, description='Model for article response.')
    def put(self, id):
        '''
        Update existing article by its ID.

        NOTE: topic_ids does not be supported in update API. Please send article update format without topic_ids.

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


parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=False, help='Search article by its title')
parser.add_argument('user_id', type=str, required=False, help='Search article by user_id (who created article)')
parser.add_argument('fixed_topic_id', type=str, required=False, help='Search all articles related to fixed-topic.')
parser.add_argument('topic_id', type=str, required=False, help='Search all articles related to topic.')
parser.add_argument('from_date', type=str, required=False, help='Search articles created later that this date.')
parser.add_argument('to_date', type=str, required=False, help='Search articles created before this data.')
parser.add_argument('anonymous', type=str, required=False, help='Search articles created by Anonymous.')


@api.route('/search')
@api.expect(parser)
class QuesstionSearch(Resource):
    @token_required
    @api.response(code=200, model=model_response, description='Model for article response.')
    def get(self):
        """
        Search all articles that satisfy conditions.
        ---------------------
        :param `title`: The name of the topics to search

        :param `user_id`: Search articles by user_id (who created article)

        :param `fixed_topic_id`: Search all articles by fixed topic ID.

        :param `from_date`: Search articles created after this date.

        :param `to_date`: Search articles created before this date.

        :param `anonymous`: Search articles created by anonymous.

        :return: List of articles satisfy search condition.
        """
        args = parser.parse_args()
        controller = ArticleController()
        return controller.search(args=args)
