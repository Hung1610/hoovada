#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.article.comment.favorite.favorite_controller import ArticleCommentFavoriteController
from app.modules.article.comment.favorite.favorite_dto import ArticleCommentFavoriteDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = ArticleCommentFavoriteDto.api
_favorite_request = ArticleCommentFavoriteDto.model_request
_favorite_response = ArticleCommentFavoriteDto.model_response
_favorite_get_params = ArticleCommentFavoriteDto.model_get_parser

@api.route('/<int:article_comment_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_favorite_get_params)
    def get(self, article_comment_id):
        """
        Search all favorite that satisfy conditions.
        """

        args = _favorite_get_params.parse_args()
        controller = ArticleCommentFavoriteController()
        return controller.get(article_comment_id=article_comment_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, article_comment_id):
        """
        Create a favorite on current user.
        """

        controller = ArticleCommentFavoriteController()
        return controller.create(article_comment_id=article_comment_id)

    @token_required
    def delete(self, article_comment_id):
        """
        Delete favorite on current user.
        """
        
        controller = ArticleCommentFavoriteController()
        return controller.delete(article_comment_id=article_comment_id)
