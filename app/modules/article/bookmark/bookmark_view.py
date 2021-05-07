#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.article.bookmark.bookmark_controller import ArticleBookmarkController
from app.modules.article.bookmark.bookmark_dto import ArticleBookmarkDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleBookmarkDto.api
_bookmark_request = ArticleBookmarkDto.model_request
_bookmark_response = ArticleBookmarkDto.model_response
_bookmark_get_params = ArticleBookmarkDto.model_get_parser

@api.route('/all/bookmark')
class BookmarkArticleAll(Resource):
    @api.expect(_bookmark_get_params)
    def get(self):
        """Get all bookmark that satisfy conditions"""

        args = _bookmark_get_params.parse_args()
        controller = ArticleBookmarkController()
        return controller.get(args=args)

@api.route('/<int:article_id>/bookmark')
class BookmarkArticle(Resource):
    @api.expect(_bookmark_get_params)
    def get(self, article_id):
        """Get all bookmarks using article_id"""

        args = _bookmark_get_params.parse_args()
        args['article_id'] = article_id
        controller = ArticleBookmarkController()
        return controller.get(args=args)

    @token_required
    @api.response(code=200, model=_bookmark_response, description='The model for bookmark.')
    def post(self, article_id):
        """Create a bookmark using article_id"""

        controller = ArticleBookmarkController()
        return controller.create(article_id=article_id)

    @token_required
    def delete(self, article_id):
        """Delete bookmark using article_id"""
        
        controller = ArticleBookmarkController()
        return controller.delete(article_id=article_id)
