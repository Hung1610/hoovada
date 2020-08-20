#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
# from app.modules.common.decorator import token_required
from app.modules.article.favorite.favorite_dto import FavoriteDto
from app.modules.article.favorite.favorite_controller import FavoriteController
from app.modules.auth.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = FavoriteDto.api
_favorite_request = FavoriteDto.model_request
_favorite_response = FavoriteDto.model_response
_vote_get_params = FavoriteDto.model_get_parser

@api.route('/<int:article_id>/favorite')
class FavoriteUser(Resource):
    @token_required
    @api.expect(_vote_get_params)
    def get(self, article_id):
        """
        Search all favorite that satisfy conditions.
        """

        args = _vote_get_params.parse_args()
        controller = FavoriteController()
        return controller.get(article_id=article_id, args=args)

    @token_required
    @api.expect(_favorite_request)
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, article_id):
        """
        Create a favorite on current user.
        """

        controller = FavoriteController()
        data = api.payload
        return controller.create(article_id=article_id, data=data)

    @token_required
    def delete(self, article_id):
        """
        Delete favorite on current user.
        """
        
        controller = FavoriteController()
        return controller.delete(article_id=article_id)
