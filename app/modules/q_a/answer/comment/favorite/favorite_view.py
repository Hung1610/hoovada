#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource, reqparse

# own modules
from app.modules.q_a.answer.comment.favorite.favorite_controller import AnswerCommentFavoriteController
from app.modules.q_a.answer.comment.favorite.favorite_dto import AnswerCommentFavoriteDto
from common.utils.decorator import token_required

__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = AnswerCommentFavoriteDto.api
_favorite_request = AnswerCommentFavoriteDto.model_request
_favorite_response = AnswerCommentFavoriteDto.model_response
_favorite_get_params = AnswerCommentFavoriteDto.model_get_parser

@api.route('/<int:answer_comment_id>/favorite')
class FavoriteUser(Resource):
    @api.expect(_favorite_get_params)
    def get(self, answer_comment_id):
        """
        Search all favorite that satisfy conditions.
        """

        args = _favorite_get_params.parse_args()
        controller = AnswerCommentFavoriteController()
        return controller.get(answer_comment_id=answer_comment_id, args=args)

    @token_required
    @api.response(code=200, model=_favorite_response, description='The model for favorite.')
    def post(self, answer_comment_id):
        """
        Create a favorite on current user.
        """

        controller = AnswerCommentFavoriteController()
        return controller.create(answer_comment_id=answer_comment_id)

    @token_required
    def delete(self, answer_comment_id):
        """
        Delete favorite on current user.
        """
        
        controller = AnswerCommentFavoriteController()
        return controller.delete(answer_comment_id=answer_comment_id)
