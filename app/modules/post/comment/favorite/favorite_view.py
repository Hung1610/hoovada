#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.post.comment.favorite.favorite_controller import PostCommentFavoriteController
from app.modules.post.comment.favorite.favorite_dto import PostCommentFavoriteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PostCommentFavoriteDto.api
_favorite_request = PostCommentFavoriteDto.model_request
_favorite_response = PostCommentFavoriteDto.model_response
_favorite_get_params = PostCommentFavoriteDto.model_get_parser

@api.route('/<int:post_comment_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_favorite_get_params)
    def get(self, post_comment_id):
        """Search all favorite that satisfy conditions.
        """

        args = _favorite_get_params.parse_args()
        controller = PostCommentFavoriteController()
        return controller.get(post_comment_id=post_comment_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, post_comment_id):
        """
        Create a favorite on current user.
        """

        controller = PostCommentFavoriteController()
        return controller.create(post_comment_id=post_comment_id)

    @token_required
    def delete(self, post_comment_id):
        """
        Delete favorite on current user.
        """
        
        controller = PostCommentFavoriteController()
        return controller.delete(post_comment_id=post_comment_id)
