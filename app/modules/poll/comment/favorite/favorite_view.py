#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.poll.comment.favorite.favorite_controller import PollCommentFavoriteController
from app.modules.poll.comment.favorite.favorite_dto import PollCommentFavoriteDto
from common.utils.decorator import admin_token_required, token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = PollCommentFavoriteDto.api
_favorite_request = PollCommentFavoriteDto.model_request
_favorite_response = PollCommentFavoriteDto.model_response
_favorite_get_params = PollCommentFavoriteDto.model_get_parser

@api.route('/<int:poll_comment_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_favorite_get_params)
    def get(self, poll_comment_id):
        """Search all favorite that satisfy conditions.
        """

        args = _favorite_get_params.parse_args()
        controller = PollCommentFavoriteController()
        return controller.get(poll_comment_id=poll_comment_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, poll_comment_id):
        """
        Create a favorite on current user.
        """

        controller = PollCommentFavoriteController()
        return controller.create(poll_comment_id=poll_comment_id)

    @token_required
    def delete(self, poll_comment_id):
        """
        Delete favorite on current user.
        """
        
        controller = PollCommentFavoriteController()
        return controller.delete(poll_comment_id=poll_comment_id)
