#!/usr/bin/env python
# -*- coding: utf-8 -*-

# built-in modules
from datetime import datetime

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.article.article_dto import ArticleDto
from app.modules.article.article_controller import ArticleController
from app.modules.auth.decorator import token_required, admin_token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleDto.api
_article_dto_request = ArticleDto.model_article_request
_article_dto_response = ArticleDto.model_article_response
_article_get_params = ArticleDto.model_get_parser
_article_get_similar_params = ArticleDto.get_similar_articles_parser

@api.route('')
class ArticleList(Resource):
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    @api.expect(_article_get_params)
    def get(self):
        """
        Get all articles that satisfy conditions
        """

        args = _article_get_params.parse_args()
        controller = ArticleController()
        return controller.get(args=args)


    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def post(self):
        """
        Create new article and save to database.
        """

        data = api.payload
        controller = ArticleController()
        return controller.create(data=data)


@api.route('/<string:id_or_slug>')
class Article(Resource):
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def get(self, id_or_slug):
        """
        Get specific article by its ID.
        """

        controller = ArticleController()
        return controller.get_by_id(object_id=id_or_slug)

    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def put(self, id_or_slug):
        """
        Update existing article by its ID.
        """

        data = api.payload
        controller = ArticleController()
        return controller.update(object_id=id_or_slug, data=data, is_put=True)

    @token_required
    @api.expect(_article_dto_request)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def patch(self, id_or_slug):
        """
        Update existing article by its ID.
        """

        data = api.payload
        controller = ArticleController()
        return controller.update(object_id=id_or_slug, data=data)

    @admin_token_required()
    def delete(self, id_or_slug):
        """
        Delete the article by its ID.
        """

        controller = ArticleController()
        return controller.delete(object_id=id_or_slug)

        
@api.route('/similar')
class ArticleSimilar(Resource):
    @api.expect(_article_get_similar_params)
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def get(self):
        """ 
        Get similar articles.
        """
        args = _article_get_similar_params.parse_args()
        controller = ArticleController()
        return controller.get_similar(args=args)


@api.route('/update_slug')
class UpdateArticleSlug(Resource):
    # @admin_token_required()
    @api.response(code=200, model=_article_dto_response, description='Model for question response.')
    def post(self):
        """ 
        Update Slug for articles in DB
        """

        controller = ArticleController()
        return controller.update_slug()

parser_article_hot = reqparse.RequestParser()
parser_article_hot.add_argument('page', type=int, required=False, help='Search articles by page.')
parser_article_hot.add_argument('per_page', type=int, required=False, help='Get record number on page.')

@api.route('/article_hot')
@api.expect(parser_article_hot)
class ArticleHot(Resource):
    @token_required
    @api.response(code=200, model=_article_dto_response, description='Model for article response.')
    def get(self):
        """ get articles hot 
        """

        args = parser.parse_args()
        controller = ArticleController()
        return controller.get_article_hot(args)
